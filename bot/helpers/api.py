from abc import ABC
from typing import Optional, Any

import requests
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from config import settings
from exceptions.api_handler import api_error_handler
from message_generators.errors.auth import user_not_authorized_message
from message_generators.errors.server import unexpected_server_error_message
from redis_cache.client import get_redis_client
from telebot.types import CallbackQuery, Message

from bot import tg_bot
from logger import logger
from schemas.exceptions import APIRequestError, UnexpectedServerError


class ApiHelper(ABC):
    """Абстрактный класс для взаимодействия с api."""

    API_URL: str = settings.api.url

    def __init__(
        self,
        message: Message | CallbackQuery,
        is_auth: bool = False,
    ):
        self.message = message
        self.headers = self.get_auth_headers_by_telegram_id_in_message(is_auth)

    def get_auth_headers_by_telegram_id_in_message(
        self, is_auth: bool = False
    ) -> dict[str, str] | None:
        """Метод для получения заголовков, для запросов к api."""
        if is_auth:
            return {}

        telegram_id = self.message.from_user.id

        redis_client = get_redis_client()
        token = redis_client.get(
            "user_token:{telegram_id}".format(telegram_id=telegram_id)
        )

        if token:
            return {"Authorization": "Bearer {token}".format(token=token)}

        tg_bot.send_message(
            self.message.chat.id,
            user_not_authorized_message,
        )
        return None

    @api_error_handler
    def _send_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> requests.Response:
        """Метод для создания запросов к api."""

        url = "{api}{endpoint}".format(api=self.API_URL, endpoint=endpoint)
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
            )
            if response.status_code == HTTP_500_INTERNAL_SERVER_ERROR:
                raise UnexpectedServerError("Непредвиденная ошибка сервера.")
            return response
        except requests.exceptions.RequestException as e:
            logger.error("Ошибка запроса: {}".format(e))
            tg_bot.send_message(
                self.message.chat.id,
                unexpected_server_error_message,
            )
            raise APIRequestError("Ошибка запроса к API")
