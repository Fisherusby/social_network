from core.repositories.base import BaseRepository
from core import models


class PostRepository(BaseRepository):
    pass


post = PostRepository(model=models.Post)
