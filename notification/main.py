import asyncio

from kafka_consumer.reminder import check_reminder_topic
from logger import logger

if __name__ == "__main__":
    logger.info("Kafka_consumer начинает свою работу.")
    asyncio.run(check_reminder_topic())
