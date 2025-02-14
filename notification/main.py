import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import settings
from logger import logger

from notification.reminders import send_reminders


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_reminders,
        "cron",
        hour=settings.notification.hour_we_remind,
        timezone=settings.notification.timezone,
    )
    # scheduler.add_job(send_reminders, "interval", seconds=5)  # Для тестов

    scheduler.start()

    logger.info("Scheduler запущен...")

    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        logger.info("Остановка...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
