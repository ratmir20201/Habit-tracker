import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from api.crud.habits import get_habit
from api.models import HabitTracking
from api.schemas.habit_tracking import HabitTrackingCreate


async def create_habit_tracking(
    session: AsyncSession,
    habit: HabitTrackingCreate,
) -> HabitTracking:
    exist_habit = await get_habit(session=session, habit_id=habit.habit_id)
    if not exist_habit:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Привычка с таким id не найдена!",
        )

    exist_tracking = await checker_habit_tracking_exist(
        session=session,
        habit_id=habit.habit_id,
    )
    if exist_tracking:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Привычка уже отмечена как выполненная сегодня!",
        )

    new_habit_tracking = HabitTracking(
        **habit.model_dump(),
        date=datetime.datetime.now(datetime.UTC).date(),
    )

    session.add(new_habit_tracking)
    await session.commit()

    return new_habit_tracking


async def checker_habit_tracking_exist(
    session: AsyncSession,
    habit_id: int,
) -> HabitTracking | None:
    today = datetime.datetime.now(datetime.UTC).date()
    query = await session.execute(
        select(HabitTracking).where(
            HabitTracking.habit_id == habit_id and HabitTracking.date == today
        ),
    )
    exist_tracking = query.scalars().first()

    return exist_tracking
