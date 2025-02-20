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
from validators.valid_untrack import valid_untracked_users_habits

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
    """
    Endpoint для получения пользователей не отметивших свои привычки.

    Может использовать только superuser.
    """

    untracked_users_habits = await get_untracked_habits(session=session)
    return await valid_untracked_users_habits(untracked_users_habits)
