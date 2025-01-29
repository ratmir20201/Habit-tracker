from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from api.crud.habits import (
    create_habit,
    get_habits_by_user_id,
    delete_habit_by_id,
    update_habit,
)
from api.database.db import get_session
from api.dependencies.habits import habit_by_id
from api.models.habit import Habit
from api.schemas.habit import HabitCreate, HabitResponse, HabitUpdate

router = APIRouter(tags=["Habits"])


@router.post(
    "/api/habits",
    status_code=HTTP_201_CREATED,
    response_model=HabitResponse,
)
async def add_habit(habit: HabitCreate, session: AsyncSession = Depends(get_session)):
    """Endpoint для создания привычки."""

    created_habit = await create_habit(session=session, habit=habit)

    return HabitResponse(result=True, data=created_habit)


@router.get(
    "/api/habits/{user_id}",
    status_code=HTTP_200_OK,
    response_model=HabitResponse,
)
async def get_all_habits_by_user_id(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Endpoint для получения всех привычек пользователя."""

    all_habits = await get_habits_by_user_id(session=session, user_id=user_id)

    return HabitResponse(result=True, data=all_habits)


@router.get(
    "/api/habits/{habit_id}",
    status_code=HTTP_200_OK,
    response_model=HabitResponse,
)
async def get_habit_by_id(habit: Habit = Depends(habit_by_id)):
    """Endpoint для получения привычки по id."""

    return HabitResponse(result=True, data=habit)


@router.patch(
    "/api/habits/{habit_id}",
    status_code=HTTP_200_OK,
    response_model=HabitResponse,
)
async def update_habit(
    habit_update: HabitUpdate,
    habit: Habit = Depends(habit_by_id),
    session: AsyncSession = Depends(get_session),
):
    """Endpoint для изменения привычки."""
    habit = await update_habit(habit=habit, session=session, habit_update=habit_update)
    return HabitResponse(result=True, data=habit)


@router.delete("/api/habits/{habit_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_habit(
    habit: Habit = Depends(habit_by_id),
    session: AsyncSession = Depends(get_session),
):
    """Endpoint для удаления привычки."""

    return await delete_habit_by_id(session=session, habit=habit)
