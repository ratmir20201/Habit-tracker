from database.db import get_session
from fastapi import Depends
from models.access_token import AccessToken
from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(session: AsyncSession = Depends(get_session)):
    yield AccessToken.get_db(session=session)
