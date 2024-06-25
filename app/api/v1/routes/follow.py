from fastapi import APIRouter
from sqlmodel import select
from app.crud import get_user_by_email
from app.models.posts import Follow, FollowCreate
from app.api.v1.deps import CurrentUser, SessionDep
from app.models.users import User, UserPublic

router = APIRouter()


@router.post("/", response_model=Follow)
def create_follow(db: SessionDep, user: CurrentUser, follow: FollowCreate):
    following = get_user_by_email(session=db, email=follow.email)
    obj = Follow(
        user_follower_id=user.id,
        user_following_id=following.id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[UserPublic])
def read_posts(db: SessionDep, user: CurrentUser):
    statement = (
        select(User)
        .join(Follow, Follow.user_following_id == User.id)
        .where(Follow.user_follower_id == user.id)
    )
    results = db.exec(statement)
    return results
