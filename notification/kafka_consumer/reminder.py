import json

from kafka_consumer.consumer import get_consumer
from logger import logger
from tg_reminder import send_reminders


async def check_reminder_topic():
    """Функция для получения сообщений из kafka."""
    async with get_consumer() as consumer:
        async for message in consumer:
            logger.info(
                "Получено сообщение от kafka: {message}".format(
                    message=message.value.decode("utf-8"),
                )
            )
            kafka_message = json.loads(message.value.decode("utf-8"))
            await send_reminders(untracked_user_habits=kafka_message)
