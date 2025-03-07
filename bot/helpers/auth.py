from config import settings
from helpers.api import ApiHelper
from redis_cache.client import get_redis_client
from schemas.register import RegisterSchema
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from telebot.types import Message


class AuthenticationHelper(ApiHelper):
    """Класс для взаимодействия с аутентификацией."""

    def __init__(self, message: Message):
        super().__init__(message, is_auth=True)

    def register_user(self, user_data: RegisterSchema) -> str | None:
        """Функция для регистрации пользователя."""

        user_dict = user_data.model_dump()
        response = self._send_request(
            method="post",
            endpoint="/auth/register",
            request_data=user_dict,
        )

        if response.status_code == HTTP_201_CREATED:
            return "success"
        elif response.status_code == HTTP_400_BAD_REQUEST:
            return "register_user_already_exist"
        return None

    def login_and_save_token_in_redis(self) -> str | None:
        """
        Функция для входа пользователя в систему.

        При авторизации пользователя мы также сохраняем его telegram_id
        как токен в redis.
        """

        telegram_id = self.message.from_user.id

        response = self._send_request(
            method="post",
            endpoint="/auth/telegram/login",
            request_params={"telegram_id": telegram_id},
        )

        if response.status_code == HTTP_201_CREATED:
            token = response.json().get("token").get("access_token")
            self._save_token_in_redis(token=token)
            return "success"
        elif response.status_code == HTTP_404_NOT_FOUND:
            return "user_not_found"
        return None

    def logout_and_delete_token_in_redis(self) -> str:
        """
        Функция для выхода пользователя из аккаунта.

        Также удаляем ранее созданный токен из redis.
        """

        redis_client = get_redis_client()
        telegram_id = self.message.from_user.id

        token_key = "user_token:{telegram_id}".format(telegram_id=telegram_id)
        if redis_client.exists(token_key):
            redis_client.delete(token_key)
            return "success"

        return "user_already_logout"

    def _save_token_in_redis(self, token: str):
        """Функция для сохранения токена в redis."""
        redis_client = get_redis_client()
        telegram_id = self.message.from_user.id
        redis_client.setex(
            name="user_token:{telegram_id}".format(telegram_id=telegram_id),
            time=settings.redis.token_expire,
            value=token,
        )
