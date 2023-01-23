from core.repositories.base import BaseRepository
from core import models

from sqlalchemy.ext.asyncio import AsyncSession


class PostRepository(BaseRepository):
    pass


post = PostRepository(model=models.Post)
