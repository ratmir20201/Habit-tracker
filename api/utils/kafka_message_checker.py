import datetime


from logger import logger
from models import KafkaMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class KafkaMessageExistsError(Exception):
    """Исключение для случая, когда kafka-сообщение уже существует."""


async def check_if_kafka_message_already_exist(
    session: AsyncSession,
    telegram_id: int,
) -> None:
    kafka_message_query = await session.execute(
        select(KafkaMessage).where(
            (KafkaMessage.telegram_id == telegram_id)
            & (KafkaMessage.date == datetime.datetime.now().date())
        ),
    )
    kafka_message = kafka_message_query.scalar_one_or_none()

    if kafka_message:
        logger.error("Такое kafka сообщение уже существует.")
        raise KafkaMessageExistsError(
            "Kafka сообщение с таким telegram_id уже отправлено сегодня."
        )
