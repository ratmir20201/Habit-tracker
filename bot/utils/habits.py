import logging
from typing import Any

import requests
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from telebot.types import Message

from main import tg_bot
from redis_cache.auth_headers import get_auth_headers_by_telegram_id_in_message
from test_config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HabitsHelper:
    API_URL: str = settings.api.url

    def __init__(self, message: Message):
        self.message = message
        self.headers = get_auth_headers_by_telegram_id_in_message(message)

    def _send_request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
    ) -> requests.Response | None:
        url = "{api}{endpoint}".format(api=self.API_URL, endpoint=endpoint)
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
            )
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса: {e}")
            tg_bot.send_message(
                self.message.chat.id, "❌ Ошибка сервера. Попробуйте позже."
            )
            return None

    def get_user_habits(self) -> list[dict[str, Any]] | None:
        response = self._send_request(method="get", endpoint="/api/habits/me")

        if response.status_code == HTTP_200_OK:
            habits = response.json()
            return habits
        elif response.status_code == HTTP_401_UNAUTHORIZED:
            return

    def add_habit(self):
        habit_name = self.message.text.strip().capitalize()
        habit_data = {"name": habit_name}

        response = self._send_request(
            method="post",
            endpoint="/api/habits",
            data=habit_data,
        )

        if response.status_code == HTTP_201_CREATED:
            habit = response.json()
            return habit
        elif response.status_code == HTTP_400_BAD_REQUEST:
            tg_bot.send_message(
                self.message.chat.id, "🚫 У вас уже имеется такая привычка."
            )
