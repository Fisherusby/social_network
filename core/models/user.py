from core.models.base import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = 'user'

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
