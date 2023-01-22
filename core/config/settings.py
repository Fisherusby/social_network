from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Social network'
    DOCS_URL: str
    VERSION: str
    API_PREFIX: str = "/api"
    VERSION: str = '0.0.1'

    SQLALCHEMY_DATABASE_URI: str

    class Config:
        case_sensitive = True


settings: Settings = Settings(_env_file=".env", _env_file_encoding="utf-8")