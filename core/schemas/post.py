from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Query
from core import schemas
from core.schemas.base import BaseAPIModel
from datetime import datetime


class BasePost(BaseAPIModel):
    """Base post model"""
    title: str
    content: str


class CreatePost(BasePost):
    pass


class UpdatePost(BaseAPIModel):
    """Update post model"""
    title: Optional[str]
    content: Optional[str]


class Author(schemas.BaseUser):
    """Post author model"""
    id: int


class LikeDislike(BaseModel):
    """Post like-dislike model"""
    like: int
    dislike: int


class Post(BasePost):
    """Post with all info model"""
    id: int
    user: Author
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    like_count: Optional[LikeDislike]
    like: Optional[bool]


class Pagination(BaseAPIModel):
    """Pagination model"""
    limit: Optional[int] = Field(Query(100), alias='limit')
    offset: Optional[int] = Field(Query(0), alias='offset')
