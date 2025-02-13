from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config import settings
import logging

logging.basicConfig(level=logging.INFO)


async def init_cache():
    """Инициализация кеша с Redis."""
    logging.info("🔄 Инициализация кеша...")
    redis = aioredis.from_url(settings.redis.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logging.info("✅ Кэш успешно инициализирован!")
