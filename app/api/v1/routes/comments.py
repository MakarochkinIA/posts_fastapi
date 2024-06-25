from fastapi import APIRouter
from typing import List
from app.models.posts import Comment, CommentBase
from app.crud import post_crud, comment_crud
from app.api.v1.deps import CurrentUser, SessionDep, CommentPermission

router = APIRouter()


@router.delete("/{id}")
def remove_comment(db: SessionDep, commemt_db: CommentPermission):
    db.delete(commemt_db)
    db.commit()
    return {'success': True}


@router.put("/{id}", response_model=Comment)
def update_comment(
    db: SessionDep, comment: CommentBase, commemt_db: CommentPermission
):
    comment = comment_crud.update(db, db_obj=commemt_db, obj_in=comment)
    return comment


@router.get("/", response_model=List[Comment])
def read_comments(db: SessionDep, skip: int = 0, limit: int = 10):
    comments = comment_crud.get_multi(db, skip=skip, limit=limit)
    return comments


@router.get("/{id}", response_model=List[Comment])
def read_comment(db: SessionDep, id: int):
    comment = comment_crud.get(db, id)
    return comment


@router.post("/", response_model=Comment)
def create_comment(
    db: SessionDep, user: CurrentUser, comment: CommentBase, post_id: int
):
    post = post_crud.get(db, post_id)
    setattr(comment, 'author_id', user.id)
    setattr(comment, 'post_id', post.id)
    return comment_crud.create(db, obj_in=comment)
