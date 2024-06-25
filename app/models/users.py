from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .posts import Post, Follow, Comment


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    posts: list["Post"] | None = Relationship(back_populates="author")
    follower: list["Follow"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "foreign_keys": "Follow.user_follower_id"
        }
    )
    following: list["Follow"] = Relationship(
        back_populates="following",
        sa_relationship_kwargs={
            "foreign_keys": "Follow.user_following_id"
        }
    )
    comments: list["Comment"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={
            "foreign_keys": "Comment.author_id"
        }
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
