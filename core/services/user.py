from core import models
from core import repositories
from core.services.base import BaseObjectService


class UserService(BaseObjectService):
    pass


user_service = UserService(repository=repositories.user)
