import datetime

from fastapi import HTTPException
from models import HabitTracking
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST


async def check_habit_tracking_already_exist(
    session: AsyncSession,
    habit_id: int,
) -> None:
    """Проверят, существует ли привычка с habit_id которая уже отмечена сегодня."""

    today = datetime.datetime.now().date()
    query = await session.execute(
        select(HabitTracking).where(
            (HabitTracking.habit_id == habit_id) & (HabitTracking.date == today)
        ),
    )
    exist_tracking = query.scalar_one_or_none()
    if exist_tracking:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Привычка уже отмечена как выполненная сегодня!",
        )
