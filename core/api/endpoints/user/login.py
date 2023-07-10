from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core import schemas, services
from core.api import depends

router = APIRouter()


@router.post('/login', status_code=200, response_model=schemas.OAuth2TokensResponse)
async def login(
    db: AsyncSession = Depends(depends.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """Endpoint to user sing in."""
    auth_data: schemas.OAuth2TokensResponse = await services.user_service.authenticate(
        db=db, email=form_data.username, password=form_data.password
    )

    return auth_data


@router.post('/refresh', status_code=200, response_model=schemas.AccessTokenResponse)
async def refresh(
    data: schemas.RefreshTokenRequest,
    db: AsyncSession = Depends(depends.get_session),
) -> Any:
    """Endpoint to user sing in."""
    access_token: schemas.AccessTokenResponse = await services.user_service.refresh_token(
        db=db, refresh_token=data.refresh_token
    )

    return access_token
