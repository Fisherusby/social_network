from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from core.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


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

    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        query = select(self.model).filter(self.model.id == id)
        res = (await db.execute(query)).scalar_one_or_none()
        return res

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

    async def delete_by_id(self, db: AsyncSession, *, id: int):
        obj = await self.get_by_id(db=db, id=id)

        query = delete(self.model).where(self.model.id == id)

        await db.execute(query)
        await db.commit()
        return obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = dict(db_obj.__dict__)
        obj_data.pop('_sa_instance_state')

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.flush()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj



