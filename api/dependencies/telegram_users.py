from database.db import get_session
from fastapi import Depends, HTTPException
from models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND


async def user_by_telegram_id(
    telegram_id: int,
    session: AsyncSession = Depends(get_session),
) -> User:
    query_user = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = query_user.scalar_one_or_none()
    if user is not None:
        return user

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail="Пользователь с telegram_id {} не был найден.".format(telegram_id),
    )
