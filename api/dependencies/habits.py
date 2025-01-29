from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from api.crud.habits import get_habit
from api.database.db import get_session
from api.models.habit import Habit


async def habit_by_id(
    habit_id: int, session: AsyncSession = Depends(get_session)
) -> Habit:
    habit = await get_habit(session=session, habit_id=habit_id)
    if habit is not None:
        return habit

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail="Привычка по id {} не была найдена.".format(habit_id),
    )
