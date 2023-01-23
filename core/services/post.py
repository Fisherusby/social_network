from core import models
from core import repositories
from core.services.base import BaseObjectService


class PostService(BaseObjectService):
    pass


post_service = PostService(repository=repositories.post)
