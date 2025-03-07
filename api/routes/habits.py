from authentication.fastapi_users_router import fastapi_users
from config import settings
from crud.habits import (create_habit, delete_habit_by_id,
                         get_habits_by_user_id, update_habit_by_id)
from database.db import get_session
from dependencies.habits import habit_by_id
from dependencies.users import user_by_id
from exceptions.habits import (add_habit_responses, delete_habit_responses,
                               get_all_my_habits_responses,
                               get_all_user_habits_responses,
                               get_habit_by_id_responses,
                               update_habit_responses)
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from models import User
from models.habit import Habit
from schemas.habit import HabitBase, HabitCreate, HabitResponse, HabitUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN)

router = APIRouter(tags=["Habits"], prefix="/habits")


@router.get(
    "/me",
    status_code=HTTP_200_OK,
    response_model=list[HabitResponse],
    responses=get_all_my_habits_responses,
)
@cache(expire=settings.api.cache_time)
async def get_all_my_habits(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    """
    Endpoint для получения всех привычек пользователя.

    Этот маршрут закэширован.
    """

    all_habits = await get_habits_by_user_id(
        session=session,
        user_id=current_user.id,
    )

    return [HabitResponse.model_validate(habit) for habit in all_habits]


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=HabitBase,
    responses=add_habit_responses,
)
async def add_habit(
    habit: HabitCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    """Endpoint для создания привычки."""

    created_habit = await create_habit(
        session=session,
        habit=habit,
        user_id=current_user.id,
    )

    return created_habit


@router.patch(
    "/{habit_id}",
    status_code=HTTP_200_OK,
    response_model=HabitResponse,
    responses=update_habit_responses,
)
async def update_habit(
    habit_update: HabitUpdate,
    current_user: User = Depends(fastapi_users.current_user()),
    habit: Habit = Depends(habit_by_id),
    session: AsyncSession = Depends(get_session),
):
    """Endpoint для изменения привычки."""
    updated_habit = await update_habit_by_id(
        habit=habit,
        session=session,
        habit_update=habit_update,
        user_id=current_user.id,
    )
    return HabitResponse.model_validate(updated_habit)


@router.get(
    "/{habit_id}",
    status_code=HTTP_200_OK,
    response_model=HabitResponse,
    responses=get_habit_by_id_responses,
)
@cache(expire=settings.api.cache_time)
async def get_habit_by_id(
    current_user: User = Depends(fastapi_users.current_user()),
    habit: Habit = Depends(habit_by_id),
):
    """
    Endpoint для получения привычки по id.

    Этот маршрут закэширован.
    """
    if habit.user_id == current_user.id:
        return HabitResponse.model_validate(habit)

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="У вас недостаточно прав для данной операции.",
    )


@router.get(
    "/user/{user_id}",
    status_code=HTTP_200_OK,
    response_model=list[HabitResponse],
    responses=get_all_user_habits_responses,
)
@cache(expire=settings.api.cache_time)
async def get_user_habits(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(user_by_id),
    current_user: User = Depends(fastapi_users.current_user(superuser=True)),
):
    """
    Endpoint для получения привычек пользователя по его id.

    Может использовать только superuser.
    """
    all_habits = await get_habits_by_user_id(
        session=session,
        user_id=user.id,
    )
    return all_habits


@router.delete(
    "/{habit_id}",
    status_code=HTTP_204_NO_CONTENT,
    responses=delete_habit_responses,
)
async def delete_habit(
    current_user: User = Depends(fastapi_users.current_user()),
    habit: Habit = Depends(habit_by_id),
    session: AsyncSession = Depends(get_session),
):
    """Endpoint для удаления привычки."""

    return await delete_habit_by_id(
        session=session,
        habit=habit,
        user_id=current_user.id,
    )
