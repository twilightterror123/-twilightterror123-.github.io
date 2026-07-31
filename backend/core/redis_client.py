import redis.asyncio as redis
from core.config import settings

class RedisPool:
    def __init__(self):
        self._client = None

    async def initialize(self):
        self._client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get(self, key: str) -> str:
        return await self._client.get(key)

    async def setex(self, key: str, time: int, value: str):
        await self._client.setex(key, time, value)

    async def close(self):
        if self._client:
            await self._client.close()

redis_pool = RedisPool()
