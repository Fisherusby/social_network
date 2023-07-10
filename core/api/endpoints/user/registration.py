from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import schemas, services
from core.api.depends import get_session

router: APIRouter = APIRouter()


@router.post(
    "",
    status_code=201,
)
async def user_registration(
    *,
    db: AsyncSession = Depends(get_session),
    data: schemas.BaseUserRegistrationRequest,
) -> dict:
    """Endpoint to registration new user."""

    await services.user_service.registration(db=db, data=data)
    return {'message': "successful"}
