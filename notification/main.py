import asyncio

from kafka_consumer.reminder import check_reminder_topic

if __name__ == "__main__":
    asyncio.run(check_reminder_topic())
