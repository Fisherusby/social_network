from pydantic import BaseConfig, BaseModel


class BaseAPIModel(BaseModel):
    """Base API model with ORM."""

    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
