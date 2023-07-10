from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, Field

from core.schemas.base import BaseAPIModel
from core.schemas.user import BaseUser


class BasePost(BaseAPIModel):
    """Base post model."""

    title: str
    content: str


class CreatePost(BasePost):
    pass


class UpdatePost(BaseAPIModel):
    """Update post model."""

    title: Optional[str]
    content: Optional[str]


class Author(BaseUser):
    """Post author model."""

    id: UUID


class LikeDislike(BaseModel):
    """Post like-dislike model."""

    like: int
    dislike: int


class Post(BasePost):
    """Post with all info model."""

    id: UUID
    user: Author
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PostWithInfo(Post):
    """Post with all info model."""

    like_count: Optional[LikeDislike]
    like: Optional[bool]


class Pagination(BaseAPIModel):
    """Pagination model."""

    limit: Optional[int] = Field(Query(100), alias='limit')
    offset: Optional[int] = Field(Query(0), alias='offset')
