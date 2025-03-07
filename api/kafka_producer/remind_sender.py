import json
from datetime import datetime

from config import settings
from crud.telegram import get_untracked_habits
from database.db import get_async_context_session
from kafka_producer.producer import get_producer
from kafka_producer.remind_generator import generate_data_for_reminder
from logger import logger
from schemas.untrack import HabitSchema
from validators.valid_untrack import valid_untracked_users_habits


async def send_reminder_to_kafka(telegram_id: int, habits: list[HabitSchema]) -> bool:
    """Отправляет сообщение в Kafka"""

    async with get_producer() as producer:
        untracked_habits_users = await generate_data_for_reminder(telegram_id, habits)

        if not untracked_habits_users:
            logger.error(
                "Kafka сообщение с таким telegram_id уже было отправлено сегодня."
            )
            return False

        message = json.dumps(untracked_habits_users)
        logger.info("Отправка сообщения в топик %s ...", settings.notification.topic)
        await producer.send_and_wait(
            settings.notification.topic, message.encode("utf-8")
        )
        log_message = json.loads(message)
        logger.info("Отправлено в Kafka: %s.", log_message)

        return True


async def daily_reminders() -> bool:
    """Проверяет время и отправляет напоминания раз в сутки"""
    async with get_async_context_session() as session:
        now = datetime.now()
        if now.hour == settings.notification.hour_we_remind:
            untracked_users_habits = await get_untracked_habits(session=session)
            valid_user_habits = await valid_untracked_users_habits(
                untracked_users_habits
            )
            for i_user_habits in valid_user_habits:
                await send_reminder_to_kafka(
                    telegram_id=i_user_habits.telegram_id,
                    habits=i_user_habits.habits,
                )

            return True

    return False
