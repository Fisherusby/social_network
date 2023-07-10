import re
from typing import Optional

from pydantic import BaseModel, EmailStr, validator

from core.schemas.base import BaseAPIModel


def validate_password(v: Optional[str]) -> Optional[str]:
    """Validate password."""
    pattern = r"^[A-Za-z\d!#$%&*+\-.<=>?@^_;\]\[~`;\(\)]{8,32}$"
    if not bool(re.match(pattern, v)) or len(v) == 0:
        raise ValueError(
            "Password must contain between 8 and 32 symbols (numbers and/or letters and/or special characters)"
        )

    return v


class RefreshTokenRequest(BaseAPIModel):
    """Refresh token request."""

    refresh_token: str


class AccessTokenResponse(BaseAPIModel):
    """Access token response."""

    access_token: str


class Email(BaseAPIModel):
    """Base User fields for registration."""

    email: EmailStr


class BaseUser(Email):
    """Base User fields for registration."""

    # username: str


class BaseUserRegistrationRequest(BaseUser):
    """A model for base user registration via Email + Password."""

    password: str

    @validator("password")
    def check_password(cls, v: str):
        return validate_password(v)


class OAuth2TokensResponse(BaseModel):
    """Response access and refresh tokens."""

    access_token: str
    refresh_token: str
    token_type: str
