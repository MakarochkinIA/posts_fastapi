from fastapi import APIRouter

from app.api.v1.routes import login, users, posts, groups, comments, follow

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(follow.router, prefix="/follows", tags=["follows"])
api_router.include_router(
    comments.router, prefix="/posts/{post_id}/comments", tags=["comments"]
)
