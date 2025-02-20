import datetime

from models import KafkaMessage
from sqlalchemy.ext.asyncio import AsyncSession
from utils.kafka_message_checker import check_if_kafka_message_already_exist


async def create_kafka_message(
    session: AsyncSession,
    telegram_id: int,
) -> KafkaMessage | None:
    is_exist = await check_if_kafka_message_already_exist(
        session=session,
        telegram_id=telegram_id,
    )
    if is_exist:
        return None

    new_kafka_message = KafkaMessage(
        telegram_id=telegram_id,
        date=datetime.datetime.now().date(),
    )

    session.add(new_kafka_message)
    await session.commit()

    return new_kafka_message
