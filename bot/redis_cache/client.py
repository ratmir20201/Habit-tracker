import redis
from redis import Redis

from config import settings


def get_redis_client() -> Redis:
    return redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        decode_responses=True,
    )
