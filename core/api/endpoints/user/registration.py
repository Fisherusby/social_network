from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core import models
from core.api.depends import get_session

router: APIRouter = APIRouter()


@router.post(
    "",
    status_code=201,
)
async def user_registration(
        *,
        db: AsyncSession = Depends(get_session),
        data: models.BaseUserRegistrationRequest,
) -> dict:
    print(data.json())
    return {'message': "successful"}
