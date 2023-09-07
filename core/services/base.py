from typing import Generic, TypeVar

from core.repositories.base import BaseRepository

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseObjectService(Generic[RepositoryType]):
    def __init__(self, repository: RepositoryType):
        self.repository: RepositoryType = repository
