import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from api.crud.habits import get_habit
from api.models import Habit, HabitTracking
from api.schemas.habit_tracking import HabitTrackingCreate
from api.utils.habit_tracking_checker import check_habit_tracking_already_exist


async def create_habit_tracking(
    session: AsyncSession,
    habit_track: HabitTrackingCreate,
    habit: Habit,
) -> HabitTracking:
    await check_habit_tracking_already_exist(
        session=session,
        habit_id=habit_track.habit_id,
    )

    new_habit_tracking = HabitTracking(
        **habit_track.model_dump(),
        date=datetime.datetime.now().date(),
    )

    session.add(new_habit_tracking)
    await session.commit()

    await session.refresh(habit)

    return new_habit_tracking
