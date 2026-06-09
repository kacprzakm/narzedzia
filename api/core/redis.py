#udostepnianie endpointom istniejace polaczenie z redisem

from collections.abc import AsyncGenerator #strict = true - bez tego nie dziala bo yield potrzebuje tego typu
#https://docs.python.org/3/library/collections.abc.html
import redis.asyncio as aioredis
from fastapi import Request

RedisClient = aioredis.Redis

async def get_redis(request: Request) -> AsyncGenerator[RedisClient, None]:
    yield request.app.state.redis