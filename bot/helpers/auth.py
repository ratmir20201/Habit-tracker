from typing import Any

import requests
import starlette
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from telebot.types import Message

from helpers.api import ApiHelper
from redis_cache.client import get_redis_client
from test_config import settings
from validators.register_validator import validate_user_data


class AuthenticationHelper(ApiHelper):
    """Класс для взаимодействия с аутентификацией."""

    def __init__(self, message: Message):
        super().__init__(message, is_auth=True)

    def register_user(self, user_data: dict[str, Any]) -> starlette.status:
        """Функция для регистрации пользователя."""
        valid_user_data = validate_user_data(self.message, user_data)
        if valid_user_data is None:
            return

        response = self._send_request(
            method="post",
            endpoint="/auth/register",
            data=valid_user_data.model_dump(),
        )

        return response.status_code

    def login_and_save_token_in_redis(self) -> starlette.status:
        """Функция для входа пользователя в систему."""
        telegram_id = self.message.from_user.id

        response = self._send_request(
            method="post",
            endpoint="/auth/telegram/login",
            params={"telegram_id": telegram_id},
        )

        if response.status_code == HTTP_200_OK:
            token = response.json()["token"]["access_token"]
            self._save_token_in_redis(token=token)
            return HTTP_200_OK
        elif response.status_code == HTTP_404_NOT_FOUND:
            return HTTP_404_NOT_FOUND

    def _save_token_in_redis(self, token: str):
        redis_client = get_redis_client()
        telegram_id = self.message.from_user.id
        redis_client.setex(
            name="user_token:{telegram_id}".format(telegram_id=telegram_id),
            time=settings.redis.token_expire,
            value=token,
        )
