from datetime import datetime, timedelta
from typing import Any, Sequence

from models import Habit, HabitTracking, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_with_telegram_id(session: AsyncSession) -> Sequence[User]:
    """Получить пользователей, у которых есть telegram_id."""
    users_query = await session.execute(
        select(User).where(User.telegram_id.isnot(None)),
    )

    return users_query.scalars().all()


async def get_untracked_habits_for_user(
    session: AsyncSession,
    user: User,
) -> dict[str, Any] | None:
    """Получает непомеченные привычки для одного пользователя."""
    yesterday = datetime.now() - timedelta(days=1)

    query = await session.execute(
        select(Habit)
        .outerjoin(
            HabitTracking,
            (Habit.id == HabitTracking.habit_id) & (HabitTracking.date >= yesterday),
        )
        .where((HabitTracking.id.is_(None)) & (Habit.user_id == user.id))
    )
    habits = query.scalars().all()

    if habits:
        return {"telegram_id": user.telegram_id, "habits": habits}

    return None


async def get_untracked_habits(session: AsyncSession) -> list[dict[str, Any]]:
    """Функция для получения непомеченных привычек пользователей с telegram_id."""

    users_with_telegram_id = await get_users_with_telegram_id(session=session)

    untracked_habits_users = []
    for i_user in users_with_telegram_id:
        user_habits = await get_untracked_habits_for_user(session=session, user=i_user)
        if user_habits:
            untracked_habits_users.append(user_habits)

    return untracked_habits_users
