from database.db import get_session
from fastapi import Depends
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield User.get_db(session=session)
