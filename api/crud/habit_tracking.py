import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from api.crud.habits import get_habit
from api.models import HabitTracking
from api.schemas.habit_tracking import HabitTrackingCreate
from api.utils.habit_tracking_checker import checker_habit_tracking_already_exist


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

    await checker_habit_tracking_already_exist(session=session, habit_id=habit.habit_id)

    new_habit_tracking = HabitTracking(
        **habit.model_dump(),
        date=datetime.datetime.now().date(),
    )

    session.add(new_habit_tracking)
    await session.commit()

    await session.refresh(exist_habit)

    return new_habit_tracking
