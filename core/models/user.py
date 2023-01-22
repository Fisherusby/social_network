import re
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


def validate_password(v: Optional[str]) -> Optional[str]:
    if v:
        pattern = r"^[A-Za-z\d!#$%&*+\-.<=>?@^_;\]\[~`;\(\)]{8,32}$"
        if not bool(re.match(pattern, v)):
            raise ValueError(
                "Password must contain between 8 and 32 symbols (numbers and/or letters and/or special characters)"
            )
        return v


class Email(BaseModel):
    email: EmailStr


class BaseUser(Email):
    """Base User fields for registration."""

    name: str
    username: str


class BaseUserRegistrationRequest(Email):
    """A model for base user registration via Email + Password."""

    password: str

    @validator("password")
    def check_password(cls, v: str):
        return validate_password(v)