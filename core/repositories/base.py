from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from core.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseRepository:
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:

        return (await db.execute(select(self.model).offset(skip).limit(limit))).scalars().all()

    async def gat_by_id(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        query = select(self.model).filter(self.model.id == id)
        return (await db.execute(query)).scalar_one_or_none()

    async def get_by_field(
            self, db: AsyncSession, *, field_name: str, value: str, only_one: bool = False,
            skip: int = 0, limit: int = 100
    ):
        query = select(self.model).filter(getattr(self.model, field_name, None) == value)
        if only_one:
            return (await db.execute(query)).scalar_one_or_none()
        else:
            return (await db.execute(query.offset(skip).limit(limit))).scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: Union[CreateSchemaType, dict]):
        obj_in: dict = dict(obj_in)
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.flush()
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def delete_by_id(self):
        pass

    async def update(self):
        pass


