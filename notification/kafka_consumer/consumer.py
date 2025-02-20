import asyncio
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer
from config import settings
from logger import logger


@asynccontextmanager
async def get_consumer():
    """Асинхронный контекстный менеджер для получения consumer."""

    consumer = AIOKafkaConsumer(
        settings.notification.topic,
        bootstrap_servers=settings.kafka.broker,
        auto_offset_reset="earliest",
        client_id=settings.notification.client_id,
    )
    try:
        await consumer.start()
        yield consumer
    except asyncio.CancelledError:
        logger.info("Задача была отменена. Kafka consumer завершает работу.")
    except Exception as exc:
        logger.error("Ошибка при работе с Kafka consumer: {exc}".format(exc=exc))
        raise
    finally:
        await consumer.stop()
