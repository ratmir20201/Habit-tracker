import redis
from config import settings


def get_redis_client() -> redis.Redis:
    """Создает инстанс Redis и возвращает."""
    return redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        decode_responses=True,
    )
