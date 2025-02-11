import json

from authentication.backend import authentication_backend
from authentication.strategy import get_database_strategy
from dependencies.telegram_users import user_by_telegram_id
from fastapi import APIRouter, Depends
from fastapi_users.authentication.strategy import DatabaseStrategy
from models import User

router = APIRouter(tags=["Telegram"])


@router.post("/telegram/login")
async def auth_telegram(
    user: User = Depends(user_by_telegram_id),
    db_strategy: DatabaseStrategy = Depends(get_database_strategy),
):
    token_data = await authentication_backend.login(db_strategy, user)
    token = json.loads(token_data.body)

    return {"token": token}
