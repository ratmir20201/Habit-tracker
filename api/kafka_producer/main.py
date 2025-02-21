import asyncio

from kafka_producer.remind_sender import daily_reminders

from logger import logger


async def schedule_reminders():
    """Запускает фоновый процесс отправки напоминаний."""
    while True:
        is_delivered = await daily_reminders()
        if is_delivered:
            await asyncio.sleep(3600 * 23)
        else:
            await asyncio.sleep(60)


if __name__ == "__main__":
    logger.info("Kafka_producer начинает свою работу.")
    asyncio.run(schedule_reminders())
