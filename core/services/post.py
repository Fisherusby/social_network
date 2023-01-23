from core import models
from core import repositories
from core.services.base import BaseObjectService


from sqlalchemy.ext.asyncio import AsyncSession


class PostService(BaseObjectService):
    pass


post_service = PostService(repository=repositories.post)
