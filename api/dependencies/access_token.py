from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import get_session
from api.models.access_token import AccessToken


async def get_access_token_db(session: AsyncSession = Depends(get_session)):
    yield AccessToken.get_db(session=session)
