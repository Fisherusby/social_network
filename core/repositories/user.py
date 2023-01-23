from core.repositories.base import BaseRepository
from core import models


class UserRepository(BaseRepository):
    pass


user = UserRepository(model=models.User)
