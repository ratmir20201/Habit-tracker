from config import settings
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from logger import logger
from redis import asyncio as aioredis


async def init_cache():
    """Инициализация кеша с Redis."""
    logger.info("Инициализация кеша...")

    redis = aioredis.from_url(settings.redis.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    logger.info("Кэш успешно инициализирован!")
