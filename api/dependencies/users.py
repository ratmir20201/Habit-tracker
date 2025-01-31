# from fastapi import Depends, HTTPException
# from starlette.status import HTTP_404_NOT_FOUND
#
# from api.database.db import get_session
# from api.models.habit import Habit
#
#
# async def user_by_id(
#     user_id: int, session: AsyncSession = Depends(get_session)
# ) -> Habit:
#     user = await get_user(session=session, user_id=user_id)
#     if user is not None:
#         return user
#
#     raise HTTPException(
#         status_code=HTTP_404_NOT_FOUND,
#         detail="Пользователь с id {} не был найден.".format(user_id),
#     )
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import get_session
from api.models.user import User


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield User.get_db(session=session)
