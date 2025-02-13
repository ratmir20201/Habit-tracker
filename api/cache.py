from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config import settings


async def init_cache():
    redis = aioredis.from_url(settings.redis.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
