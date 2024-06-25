from fastapi import APIRouter, Depends
from typing import List
from app.models.posts import Group, GroupBase
from app.crud import group_crud
from app.api.v1.deps import SessionDep, get_current_active_superuser

router = APIRouter()


@router.get("/", response_model=List[Group])
def read_groups(db: SessionDep, skip: int = 0, limit: int = 10):
    groups = group_crud.get_multi(db, skip=skip, limit=limit)
    return groups


@router.get("/{id}", response_model=List[Group])
def read_group(db: SessionDep, id: int):
    group = group_crud.get(db, id)
    return group


@router.put(
        "/{id}",
        dependencies=[Depends(get_current_active_superuser)],
        response_model=Group,
)
def update_group(db: SessionDep, id: int, group_create: GroupBase):
    group = db.get(Group, id)
    group = group_crud.update(db, db_obj=group, obj_in=group_create)
    return group


@router.post(
        "/",
        dependencies=[Depends(get_current_active_superuser)],
        response_model=Group
)
def create_group(group: GroupBase, db: SessionDep):
    return group_crud.create(db, obj_in=group)


@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def remove_group(db: SessionDep, id: int):
    group = db.get(Group, id)
    db.delete(group)
    db.commit()
    return {'success': True}
