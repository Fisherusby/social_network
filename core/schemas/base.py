from pydantic import BaseConfig, BaseModel


class BaseAPIModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
