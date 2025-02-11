from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from api.authentication.fastapi_users_router import fastapi_users
from api.crud.habit_tracking import create_habit_tracking
from api.database.db import get_session
from api.dependencies.habits import habit_by_id
from api.exceptions.habit_tracking import add_habit_tracking_responses
from api.models import User
from api.schemas.habit_tracking import (HabitTrackingCreate,
                                        HabitTrackingResponse)

router = APIRouter(tags=["HabitTracking"], prefix="/track_habit")


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=HabitTrackingResponse,
    responses=add_habit_tracking_responses,
)
async def add_habit_tracking(
    habit_track: HabitTrackingCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    """Endpoint для создания трекера привычки."""
    habit = await habit_by_id(session=session, habit_id=habit_track.habit_id)
    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="У вас недостаточно прав для данной операции.",
        )

    created_habit_tracking = await create_habit_tracking(
        session=session,
        habit_track=habit_track,
        habit=habit,
    )

    return created_habit_tracking
