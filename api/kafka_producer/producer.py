import asyncio
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from config import settings
from logger import logger


@asynccontextmanager
async def get_producer():
    """Асинхронный контекстный менеджер для получения producer."""

    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka.broker,
        client_id=settings.notification.client_id,
    )
    try:
        await producer.start()
        yield producer
    except asyncio.CancelledError:
        logger.info("Задача была отменена. Kafka consumer завершает работу.")
    except Exception as exc:
        logger.error("Ошибка при работе с Kafka consumer: {exc}".format(exc=exc))
        raise
    finally:
        await producer.stop()
