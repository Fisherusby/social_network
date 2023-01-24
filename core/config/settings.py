from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Social network'
    DOCS_URL: str
    VERSION: str
    API_PREFIX: str = "/api"
    VERSION: str = '0.0.1'

    SECRET_KEY: str

    ACCESS_TOKEN_DURATION_DAYS: str = 365
    REFRESH_TOKEN_DURATION_DAYS: str = 365

    ACCESS_TOKEN_DURATION: dict = {
        "access_token": ACCESS_TOKEN_DURATION_DAYS,
        "refresh_token": REFRESH_TOKEN_DURATION_DAYS,
    }

    SQLALCHEMY_DATABASE_URI: str

    class Config:
        case_sensitive = True


settings: Settings = Settings(_env_file=".env", _env_file_encoding="utf-8")