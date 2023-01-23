from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union


from core.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self):
        pass

    def gat_by_id(self):
        pass

    def get_by_field(self):
        pass

    def create(self):
        pass

    def delete_by_id(self):
        pass

    def update(self):
        pass


