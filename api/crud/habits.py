from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from api.models.habit import Habit
from api.schemas.habit import HabitCreate, HabitUpdate


async def create_habit(
    session: AsyncSession,
    habit: HabitCreate,
    user_id: int,
) -> Habit:
    habit_query = await session.execute(
        select(Habit)
        .options(
            joinedload(Habit.user),
        )
        .where(Habit.name == habit.name and Habit.user_id == user_id),
    )
    exist_habit = habit_query.scalar_one_or_none()

    if exist_habit:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Привычка с таким именем уже существует.",
        )

    new_habit = Habit(**habit.model_dump(), user_id=user_id)

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
    habit_query = await session.execute(
        select(Habit)
        .options(
            joinedload(Habit.user),
        )
        .where(Habit.id == habit_id),
    )
    habit = habit_query.scalar_one_or_none()

    return habit


async def update_habit_by_id(
    habit: Habit,
    session: AsyncSession,
    habit_update: HabitUpdate,
    user_id: int,
) -> Habit:
    if habit.user_id == user_id:
        for name, value in habit_update.model_dump(exclude_unset=True).items():
            setattr(habit, name, value)
        await session.commit()
        return habit

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="У вас недостаточно прав для данной операции.",
    )


async def delete_habit_by_id(
    habit: Habit,
    session: AsyncSession,
    user_id: int,
) -> None:
    if habit.user_id == user_id:
        await session.delete(habit)
        await session.commit()
        return

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="У вас недостаточно прав для данной операции.",
    )
