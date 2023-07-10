from fastapi import APIRouter

from core.api.endpoints import (
    content_router,
    user_login_router,
    user_registration_router,
)

router: APIRouter = APIRouter()

router.include_router(user_registration_router, prefix='/registration', tags=['registration'])
router.include_router(user_login_router, prefix='/auth', tags=['login'])
router.include_router(content_router, prefix='/content', tags=['content'])
