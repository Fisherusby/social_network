from sqlalchemy.ext.asyncio import AsyncSession
from core.db import async_session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from core import models, services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_session() -> AsyncSession:
    """Session dependent injection"""
    async with async_session() as session:
        yield session


async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)) -> models.User:
    """Return current user by access_token."""
    token_data = services.jwt_service.decode(token=token)
    current_user: models.User = await services.user_service.get_user_for_auth(db=db, id=token_data.get('id'))
    return current_user
