from config import settings
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from logger import logger
from redis import asyncio as aioredis
from redis.asyncio.client import Redis


async def init_cache():
    """Инициализация кеша с Redis."""
    logger.info("Инициализация кеша...")

    redis: Redis = aioredis.from_url(settings.redis.redis_url)  # type: ignore
    await redis.ping()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    logger.info("Кэш успешно инициализирован!")
