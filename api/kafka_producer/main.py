import asyncio

from kafka_producer.reminder import daily_reminders


async def schedule_reminders():
    """Запускает фоновый процесс отправки напоминаний."""
    while True:
        await daily_reminders()
        await asyncio.sleep(3600 * 24)


if __name__ == "__main__":
    asyncio.run(schedule_reminders())
