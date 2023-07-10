from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt

from core.config import settings


class JWT:
    def __init__(self, algorithm: str = "HS256"):
        self.algorithm = algorithm

    def encode(self, data: dict, token_type: str) -> str:
        """Encode JWT token."""
        to_encode = data.copy()

        token_duration = settings.ACCESS_TOKEN_DURATION.get(token_type, None)

        if token_duration:
            expire = datetime.utcnow() + timedelta(days=token_duration)
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error. Invalid token type.")

        to_encode.update({"exp": expire, 'token': token_type})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, token) -> dict:
        """Decode JWT token."""
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=[self.algorithm])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return data


jwt_service = JWT()
