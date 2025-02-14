from authentication.fastapi_users_router import fastapi_users
from config import settings
from crud.telegram import get_untracked_habits
from database.db import get_session
from exceptions.untracked_users import untracked_users_responses
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from models import User
from schemas.untrack import HabitSchema, TrackingSchema, UntrackResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

router = APIRouter(tags=["Telegram"], prefix="/telegram")


@router.get(
    "/untracked_users",
    status_code=HTTP_200_OK,
    response_model=list[UntrackResponseSchema],
    responses=untracked_users_responses,
)
@cache(expire=settings.api.cache_time)
async def untracked_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(fastapi_users.current_user(superuser=True)),
):
    untracked_users_habits = await get_untracked_habits(session=session)

    result = []

    for i_user_habits in untracked_users_habits:
        habits = i_user_habits["habits"]
        validate_habits = [
            HabitSchema(
                id=habit.id,
                name=habit.name,
                tracking=[TrackingSchema(date=track.date) for track in habit.tracking],
            )
            for habit in habits
        ]
        result.append(
            UntrackResponseSchema(
                telegram_id=i_user_habits["telegram_id"],
                habits=validate_habits,
            )
        )

    return result
