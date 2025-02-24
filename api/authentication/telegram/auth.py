import json

from starlette.status import HTTP_201_CREATED

from authentication.backend import authentication_backend
from authentication.strategy import get_database_strategy
from dependencies.telegram_users import user_by_telegram_id
from fastapi import APIRouter, Depends
from fastapi_users.authentication.strategy import DatabaseStrategy

from exceptions.telegram_login import auth_telegram_responses
from models import User, AccessToken

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
    token_data = await authentication_backend.login(db_strategy, user)
    token = json.loads(token_data.body)

    return {"token": token}
