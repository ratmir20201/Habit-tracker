from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.models.habit import Habit
from api.schemas.habit import HabitCreate, HabitUpdate


async def create_habit(session: AsyncSession, habit: HabitCreate) -> Habit:
    new_habit = Habit(name=habit.name, user_id=habit.user_id)

    session.add(new_habit)
    await session.commit()

    return new_habit


async def get_habits_by_user_id(
    session: AsyncSession,
    user_id: int,
) -> list[Habit]:
    habits_query = await session.execute(
        select(Habit)
        .options(
            joinedload(Habit.user),
        )
        .where(Habit.user_id == user_id),
    )
    habits = habits_query.scalars().all()

    return habits


async def get_habit(session: AsyncSession, habit_id: int) -> Habit | None:
    return await session.get(Habit, habit_id)


async def update_habit(
    habit: Habit,
    session: AsyncSession,
    habit_update: HabitUpdate,
) -> Habit:
    for name, value in habit_update.model_dump(exclude_unset=True).items():
        setattr(habit, name, value)
    await session.commit()
    return habit


async def delete_habit_by_id(
    session: AsyncSession,
    habit: Habit,
) -> None:
    await session.delete(habit)
    await session.commit()
