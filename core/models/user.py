from sqlalchemy import Column, String

from core.models.base import Base


class User(Base):
    __tablename__ = 'user'

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
