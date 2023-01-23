from .base import Base
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
