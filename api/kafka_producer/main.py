import asyncio

from kafka_producer.remind_sender import daily_reminders
from logger import logger

HOUR_IN_SECONDS = 3600
HOURS = 23

DELIVERED_SLEEP_TIME = HOUR_IN_SECONDS * HOURS
UNDELIVERED_SLEEP_TIME = 60


async def schedule_reminders() -> None:
    """Запускает фоновый процесс отправки напоминаний."""
    while True:
        is_delivered = await daily_reminders()
        if is_delivered:
            await asyncio.sleep(DELIVERED_SLEEP_TIME)
        else:
            await asyncio.sleep(UNDELIVERED_SLEEP_TIME)


if __name__ == "__main__":
    logger.info("Kafka_producer начинает свою работу.")
    try:
        asyncio.run(schedule_reminders())
    except KeyboardInterrupt:
        logger.info("Kafka_producer остановлен пользователем.")
