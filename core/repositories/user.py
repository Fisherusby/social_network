from core.repositories.base import BaseRepository
from core import models
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, TypeVar
from pydantic import BaseModel
from core.config import security

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class UserRepository(BaseRepository):

    async def get_by_email(self, db: AsyncSession, *, email: str):
        return await self.get_by_field(db=db, field_name='email', value=email, only_one=True)

    async def create(self, db: AsyncSession, *, obj_in: Union[CreateSchemaType, dict]):
        create_data: dict = dict(obj_in)

        password = create_data.pop('password', None)
        if password:
            create_data["password_hash"] = security.get_password_hash(password)

        return await super().create(db=db, obj_in=create_data)


user = UserRepository(model=models.User)
