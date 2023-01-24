from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import as_declarative
from sqlalchemy.sql import func


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True)
    __name__: str

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def dict(self):
        return self.__dict__
