from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from authentication.fastapi_users_router import fastapi_users
from crud.habits import get_habits_by_user_id
from database.db import get_session
from models import User

router = APIRouter(tags=["Telegram"], prefix="/telegram")


@router.get(
    "/untracked_users",
    status_code=HTTP_200_OK,
)
async def untracked_users():
    pass
