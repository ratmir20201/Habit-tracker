from fastapi import HTTPException
from models.habit import Habit
from schemas.habit import HabitCreate, HabitUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette.status import HTTP_403_FORBIDDEN
from utils.habit_checker import check_if_habit_already_exist


async def create_habit(
    session: AsyncSession,
    habit: HabitCreate,
    user_id: int,
) -> Habit:
    """Создает объект привычки(Habit)."""

    await check_if_habit_already_exist(
        session=session,
        habit_name=habit.name,
        user_id=user_id,
    )

    new_habit = Habit(**habit.model_dump(), user_id=user_id)

    session.add(new_habit)
    await session.commit()

    return new_habit


async def get_habits_by_user_id(
    session: AsyncSession,
    user_id: int,
) -> list[Habit]:
    """Отдаёт все привычки(Habit) пользователя по user_id."""

    habits_query = await session.execute(
        select(Habit)
        .options(
            joinedload(Habit.user),
            selectinload(Habit.tracking),
        )
        .where(Habit.user_id == user_id)
    )
    habits = habits_query.unique().scalars().all()

    return sorted(habits, key=lambda habit: habit.streak, reverse=True)


async def get_habit(session: AsyncSession, habit_id: int) -> Habit | None:
    """Отдаёт все привычку(Habit) по ее id."""

    habit_query = await session.execute(
        select(Habit)
        .options(
            joinedload(Habit.user),
            selectinload(Habit.tracking),
        )
        .where(Habit.id == habit_id),
    )
    habit = habit_query.unique().scalar_one_or_none()

    return habit


async def update_habit_by_id(
    habit: Habit,
    session: AsyncSession,
    habit_update: HabitUpdate,
    user_id: int,
) -> Habit:
    """Изменяет объект привычки(Habit)."""

    await check_if_habit_already_exist(
        session=session,
        habit_name=habit_update.name,
        user_id=user_id,
    )

    if habit.user_id == user_id:
        for name, updated_value in habit_update.model_dump(exclude_unset=True).items():
            setattr(habit, name, updated_value)
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
    """Удаляет объект привычки(Habit)."""

    if habit.user_id == user_id:
        await session.delete(habit)
        await session.commit()
        return

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="У вас недостаточно прав для данной операции.",
    )
