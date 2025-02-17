from crud.kafka_message import create_kafka_message
from database.db import get_async_context_session
from schemas.untrack import HabitSchema


async def generate_data_for_reminder(telegram_id: int, habits: list[HabitSchema]):
    async with get_async_context_session() as session:
        await create_kafka_message(session=session, telegram_id=telegram_id)

    data = {
        "telegram_id": telegram_id,
        "habits": [
            {
                "id": habit.id,
                "name": habit.name,
                "tracking": [str(track.date) for track in habit.tracking],
            }
            for habit in habits
        ],
    }

    return data
