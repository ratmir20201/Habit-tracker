from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_400_BAD_REQUEST

from api.models import Habit


async def check_if_habit_already_exist(
    session: AsyncSession,
    habit_name: str,
    user_id: int,
) -> None:
    habit_query = await session.execute(
        select(Habit)
        .options(
            joinedload(Habit.user),
        )
        .where((Habit.name == habit_name) & (Habit.user_id == user_id)),
    )
    exist_habit = habit_query.scalar_one_or_none()

    if exist_habit:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Привычка с таким именем уже существует.",
        )
