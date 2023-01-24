from core import repositories, models, services, schemas
from core.config import settings
from core.services.base import BaseObjectService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from core.config import security
from core.config.security import verify_password, get_password_hash


class UserService(BaseObjectService):

    async def registration(self, db: AsyncSession, data):
        is_exist = await self.repository.get_by_email(db=db, email=data.email)
        print(is_exist)
        if is_exist is not None:
            raise HTTPException(
                status_code=400, detail=f"User already exist")

        await self.repository.create(db=db, obj_in=data)

    async def delete(self, db, id):
        return await self.repository.delete_by_id(db=db, id=id)

    async def get_user_for_auth(self, db: AsyncSession, id: int):
        if id is None:
            raise HTTPException(status_code=404, detail=f"User not found")

        user: models.User = await self.repository.get_by_id(db=db, id=id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User not found")
        else:
            return user

    async def authenticate(self, db: AsyncSession, email: str, password: str):
        user: models.User = await self.repository.get_by_field(db=db, field_name='email', value=email, only_one=True)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User not found")

        if verify_password(password, user.password_hash):
            token_data = {
                'id': user.id,
            }
            response = {
                "token_type": "Bearer",
                "access_token": services.jwt_service.encode(data=token_data, token_type='access_token'),
                "refresh_token": services.jwt_service.encode(data=token_data, token_type='refresh_token'),
            }
            print(f'{response=}')
            return schemas.OAuth2TokensResponse(**response)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


user_service = UserService(repository=repositories.user)
