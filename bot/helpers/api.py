import logging
from abc import ABC

import requests
from config import settings
from message_generators.errors.auth import user_not_authorized_message
from message_generators.errors.unexpected import \
    unexpected_server_error_message
from redis_cache.client import get_redis_client
from telebot.types import CallbackQuery, Message

from bot import tg_bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    def _send_request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
    ) -> requests.Response | None:
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
            return response
        except requests.exceptions.RequestException as e:
            logger.error("Ошибка запроса: {}".format(e))
            tg_bot.send_message(
                self.message.chat.id,
                unexpected_server_error_message,
            )
            return None
