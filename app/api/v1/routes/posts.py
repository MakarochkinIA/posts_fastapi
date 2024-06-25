from datetime import datetime
import json
from fastapi import APIRouter, Depends
from sqlalchemy import event
from sqlmodel import select
from app.api.v1.utils import item_check
from app.core.config import settings
from app.core.redis_service import aredis_client, redis_client
from app.models.posts import Post, PostBase, Follow
from app.crud import post_crud
from app.api.v1.deps import (
    CurrentUser, RedisClient, SessionDep, PostPermission
)
from redis.asyncio.client import Redis

from app.models.users import User
router = APIRouter()


@event.listens_for(Post, "after_insert")
def after_insert_post(mapper, connection, target):
    stmt = (
        select(User.id)
        .join(Follow, Follow.user_follower_id == User.id)
        .where(Follow.user_following_id == target.author_id)
    )

    result = connection.execute(stmt)

    # Extracting the list of IDs from the result
    user_ids = [row[0] for row in result.all()]
    print('user_ids = ', user_ids)
    redis_client().publish(settings.PUSH_NOTIFICATIONS_CHANNEL, json.dumps({
        "recievers": user_ids,
        "message": f"Post {target.id} by {target.author_id} is published"
    }))


@router.delete("/{id}")
def remove_post(db: SessionDep, post_db: PostPermission):
    db.delete(post_db)
    db.commit()
    return {'success': True}


@router.put("/{id}", response_model=Post)
def update_post(db: SessionDep, post: PostBase, post_db: PostPermission):
    post = post_crud.update(db, db_obj=post_db, obj_in=post)
    return post


@router.get("/", response_model=list[Post])
def read_posts(db: SessionDep, skip: int = 0, limit: int = 10, ):
    posts = post_crud.get_multi(db, skip=skip, limit=limit)
    return posts


@router.get("/follow", response_model=list[Post])
def read_follow_posts(
    db: SessionDep, user: CurrentUser, skip: int = 0, limit: int = 10
):
    statement = (
        select(Post)
        .join(Follow, Follow.user_following_id == Post.author_id)
        .where(Follow.user_follower_id == user.id)
    ).offset(skip).limit(limit)
    results = db.exec(statement)
    return results


@router.get("/{id}", response_model=Post)
def read_post(db: SessionDep, id: int):
    post = db.get(Post, id)
    item_check(post)
    return post


@router.post("/", response_model=Post)
def create_post(db: SessionDep, user: CurrentUser, post: PostBase):
    setattr(post, 'author_id', user.id)
    return post_crud.create(db, obj_in=post)


@router.post('/anotify')
async def anotify(redis: Redis = Depends(aredis_client)):
    await redis.publish(
        settings.PUSH_NOTIFICATIONS_CHANNEL, str(datetime.now())
    )


@router.post('/notify')
def notify(redis: RedisClient):
    redis.publish(settings.PUSH_NOTIFICATIONS_CHANNEL, str(datetime.now()))
