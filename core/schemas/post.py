from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Query
from core import schemas
from core.schemas.base import BaseAPIModel
from datetime import datetime


class BasePost(BaseAPIModel):
    title: str
    content: str


class CreatePost(BasePost):
    pass


class UpdatePost(BaseAPIModel):
    title: Optional[str]
    content: Optional[str]


class Author(schemas.BaseUser):
    id: int


class Post(BasePost):
    id: int
    user: Author
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Pagination(BaseAPIModel):
    limit: Optional[int] = Field(Query(100), alias='limit')
    offset: Optional[int] = Field(Query(0), alias='offset')
