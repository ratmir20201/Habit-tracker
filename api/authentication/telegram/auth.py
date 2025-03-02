import json

from authentication.backend import authentication_backend
from authentication.strategy import get_database_strategy
from dependencies.telegram_users import user_by_telegram_id
from exceptions.telegram_login import auth_telegram_responses
from fastapi import APIRouter, Depends
from fastapi_users.authentication.strategy import DatabaseStrategy
from models import AccessToken, User
from starlette.status import HTTP_201_CREATED

router = APIRouter(tags=["Telegram"])


@router.post(
    "/telegram/login",
    status_code=HTTP_201_CREATED,
    responses=auth_telegram_responses,
)
async def auth_telegram(
    user: User = Depends(user_by_telegram_id),
    db_strategy: DatabaseStrategy[User, int, AccessToken] = Depends(
        get_database_strategy
    ),
):
    """Роут для авторизации пользователя с помощью telegram_id."""
    token_data = await authentication_backend.login(db_strategy, user)
    token = json.loads(token_data.body)

    return {"token": token}
