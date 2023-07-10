from typing import TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core import models
from core.config import security
from core.repositories.base import BaseRepository

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class UserRepository(BaseRepository):
    async def get_by_email(self, db: AsyncSession, *, email: str):
        """Get user by email."""
        return await self.get_by_field(db=db, field_name='email', value=email, only_one=True)

    async def create(self, db: AsyncSession, *, obj_in: Union[CreateSchemaType, dict]):
        """Create user with hashed password."""
        create_data: dict = dict(obj_in)

        password = create_data.pop('password', None)
        if password:
            create_data["password_hash"] = security.get_password_hash(password)

        return await super().create(db=db, obj_in=create_data)


user = UserRepository(model=models.User)
