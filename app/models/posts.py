from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship, text
from datetime import datetime
from .users import User


class GroupBase(SQLModel):
    title: str = Field(max_length=200)
    slug: str = Field(unique=True)
    description: str


class Group(GroupBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    posts: list["Post"] | None = Relationship(back_populates="group")


class PostBase(SQLModel):
    text: str
    image: str | None = Field(default=None)
    author_id: int | None = Field(
        default=None,
        foreign_key="user.id"
    )
    group_id: int | None = Field(
        default=None,
        foreign_key="group.id"
    )


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pub_date: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    group: "Group" = Relationship(back_populates="posts")

    author: User | None = Relationship(back_populates="posts")
    comments: list["Comment"] | None = Relationship(back_populates="post")


class FollowBase(SQLModel):
    __table_args__ = (
        UniqueConstraint(
            "user_follower_id", "user_following_id", name="user_follow_author"
        ),
    )


class FollowCreate(FollowBase):
    email: str


class Follow(FollowBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_follower_id: int | None = Field(
        default=None,
        foreign_key="user.id"
    )
    user_following_id: int | None = Field(
        default=None,
        foreign_key="user.id"
    )
    user: User = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={
            "foreign_keys": "Follow.user_follower_id"
        }
    )
    following: User = Relationship(
        back_populates="following",
        sa_relationship_kwargs={
            "foreign_keys": "Follow.user_following_id"
        }
    )


class CommentBase(SQLModel):
    text: str
    author_id: int | None = Field(
        default=None,
        foreign_key="user.id"
    )
    created: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    post_id: int | None = Field(
        default=None,
        foreign_key="post.id"
    )


class Comment(CommentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    author: User = Relationship(
        back_populates="comments",
        sa_relationship_kwargs={
            "foreign_keys": "Comment.author_id"
        }
    )

    post: Post = Relationship(back_populates="comments")
