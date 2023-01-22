from fastapi import APIRouter
from core import models

router: APIRouter = APIRouter()


@router.post(
    "",
    status_code=201,
)
async def user_registration(
        *,
        data: models.BaseUserRegistrationRequest,
) -> dict:
    print(data.json())
    return {'message': "successful"}
