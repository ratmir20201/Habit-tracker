import redis
from config import settings


def get_redis_client():
    redis_client = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        decode_responses=True,
    )
    try:
        return redis_client
    finally:
        redis_client.close()
