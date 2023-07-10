from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core import models, services
from core.db import async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
reusable_oauth2_not_error = OAuth2PasswordBearer(tokenUrl=f"/api/auth/login", auto_error=False)


async def get_session() -> AsyncSession:
    """Session dependent injection."""
    async with async_session() as session:
        yield session


async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)) -> models.User:
    """Return current user by access_token."""
    token_data = services.jwt_service.decode(token=token)
    current_user: models.User = await services.user_service.get_user_for_auth(db=db, user_id=token_data.get('id'))
    return current_user


async def get_current_user_or_none(
    db: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2_not_error)
) -> Optional[models.User]:
    """Return current user or anonymous user by access_token."""
    if token is None:
        return None
    current_user: models.User = await get_current_user(db=db, token=token)
    return current_user
