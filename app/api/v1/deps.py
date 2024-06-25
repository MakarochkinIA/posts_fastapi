from collections.abc import Generator

from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from redis.client import Redis
from sqlmodel import Session
from typing import Annotated, Any, Callable, Type

from app.api.v1.utils import item_check
from app.core import security
from app.core.config import settings
from app.core.database import engine
from app.core.redis_service import redis_client
from app.models.token import TokenPayload
from app.models.users import User
from app.models.posts import Post, Group, Comment


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def model_object_access(model: Type[Any]) -> Callable:
    def _get_item(
        db: SessionDep,
        user: CurrentUser,
        id: int = Path(...),
    ):
        item = db.get(model, id)
        item_check(item)
        if not user.is_superuser and (item.author_id != user.id):
            raise HTTPException(
                status_code=403, detail="Not enough permissions"
            )
        return item

    return _get_item


PostPermission = Annotated[Post, Depends(model_object_access(Post))]
GroupPermission = Annotated[Post, Depends(model_object_access(Group))]
CommentPermission = Annotated[Post, Depends(model_object_access(Comment))]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


RedisClient = Annotated[Redis, Depends(redis_client)]
