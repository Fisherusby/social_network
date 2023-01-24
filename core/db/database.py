from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config.settings import settings


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
