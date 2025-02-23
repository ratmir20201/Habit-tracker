from datetime import date, datetime, timedelta
from typing import Any, Sequence

from models import Habit, HabitTracking, User
from schemas.untrack import HabitSchema, TrackingSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_with_telegram_id(session: AsyncSession) -> Sequence[User]:
    """Получить пользователей, у которых есть telegram_id."""
    users_query = await session.execute(
        select(User).where(User.telegram_id.isnot(None)),
    )

    return users_query.scalars().all()


async def get_untracked_habits(session: AsyncSession) -> list[dict[str, Any]]:
    """Функция для получения непомеченных привычек пользователей с telegram_id."""

    users_with_telegram_id = await get_users_with_telegram_id(session=session)
    last_24_hours = datetime.now() - timedelta(days=1)

    untracked_habits = []
    for i_user in users_with_telegram_id:
        query = await session.execute(
            select(Habit)
            .outerjoin(
                HabitTracking,
                (Habit.id == HabitTracking.habit_id)
                & (HabitTracking.date >= last_24_hours),
            )
            .where((HabitTracking.id.is_(None)) & (Habit.user_id == i_user.id))
        )
        habits = query.scalars().all()

        if habits:
            untracked_habits.append(
                {
                    "telegram_id": i_user.telegram_id,
                    "habits": habits,
                }
            )

    return untracked_habits
