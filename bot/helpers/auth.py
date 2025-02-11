from typing import Any

import starlette
from config import settings
from helpers.api import ApiHelper
from redis_cache.client import get_redis_client
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from telebot.types import Message
from validators.register_validator import validate_user_data


class AuthenticationHelper(ApiHelper):
    """Класс для взаимодействия с аутентификацией."""

    def __init__(self, message: Message):
        super().__init__(message, is_auth=True)

    def register_user(self, user_data: dict[str, Any]) -> str:
        """Функция для регистрации пользователя."""
        valid_user_data = validate_user_data(self.message, user_data)
        if valid_user_data is None:
            return

        response = self._send_request(
            method="post",
            endpoint="/auth/register",
            data=valid_user_data.model_dump(),
        )

        if response.status_code == HTTP_201_CREATED:
            return "success"
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return "register_user_already_exist"

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
        """Функция для сохранения токена в redis."""
        redis_client = get_redis_client()
        telegram_id = self.message.from_user.id
        redis_client.setex(
            name="user_token:{telegram_id}".format(telegram_id=telegram_id),
            time=settings.redis.token_expire,
            value=token,
        )

    def logout_and_delete_token_in_redis(self) -> str:
        """Функция для выхода пользователя из аккаунта."""
        redis_client = get_redis_client()
        telegram_id = self.message.from_user.id

        token_key = "user_token:{telegram_id}".format(telegram_id=telegram_id)
        if redis_client.exists(token_key):
            redis_client.delete(token_key)
            return "success"

        return "user_already_logout"
