from fastapi import APIRouter
from core.api.endpoints import user_registration_router


router: APIRouter = APIRouter()

router.include_router(user_registration_router, prefix='/registration', tags=['registration'])

