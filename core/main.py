from fastapi import FastAPI

from core.api import api
from core.config.settings import settings

app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME, version=settings.VERSION, docs_url=settings.DOCS_URL, redoc_url=None
)
app.include_router(api.router, prefix=settings.API_PREFIX)
