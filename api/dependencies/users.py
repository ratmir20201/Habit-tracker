from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import get_session
from api.models.user import User


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield User.get_db(session=session)
