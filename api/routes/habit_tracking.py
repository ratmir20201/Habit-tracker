from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from api.authentication.fastapi_users_router import fastapi_users
from api.crud.habit_tracking import create_habit_tracking
from api.database.db import get_session
from api.models import User
from api.schemas.habit_tracking import (HabitTrackingCreate,
                                        HabitTrackingResponse)

router = APIRouter(tags=["HabitTracking"], prefix="/track_habit")


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=HabitTrackingResponse,
)
async def add_habit_tracking(
    habit: HabitTrackingCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    """Endpoint для создания трекера привычки."""

    created_habit_tracking = await create_habit_tracking(
        session=session,
        habit=habit,
    )

    return created_habit_tracking
