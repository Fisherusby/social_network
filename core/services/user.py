from core import models
from core import repositories
from core.services.base import BaseObjectService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from core.config import security


class UserService(BaseObjectService):

    async def registration(self, db: AsyncSession, data):
        is_exist = await self.repository.get_by_email(db=db, email=data.email)
        print(is_exist)
        if is_exist is not None:
            raise HTTPException(
                status_code=400, detail=f"User already exist")

        await self.repository.create(db=db, obj_in=data)


user_service = UserService(repository=repositories.user)
