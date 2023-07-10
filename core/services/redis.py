from typing import Any, Optional

import aioredis

from core.config import settings


class Redis:
    """Redis instance to interact with cached data."""

    def __init__(self, url: str, password: str):
        self.app = aioredis.from_url(url, password=password, decode_responses=True)

    async def get(self, key: Any) -> Optional[str]:
        """Return value by key."""

        return await self.app.get(key)

    async def set(self, key: Any, value: Any) -> bool:
        """Set value by key."""

        if value is None:
            value = str(value)

        await self.app.set(name=key, value=value)
        return True

    async def rename_key(
        self,
        old_name: Any,
        new_name: Any,
    ):
        """Change old key by new key."""

        await self.app.rename(old_name, new_name)
        return True

    async def incrby(
        self,
        key: Any,
        amount: int,
    ):
        """Increments the key by a specified amount."""

        await self.app.incrby(key, amount)
        return True

    async def decrby(
        self,
        key: Any,
        amount: int,
    ):
        """Decrements the key by a specified amount."""

        await self.app.decrby(key, amount)
        return True


redis_service = Redis(url=f"redis://{settings.REDIS_HOST}", password=settings.REDIS_PASSWORD)
