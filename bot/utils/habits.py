import requests
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from telebot.types import Message

from main import tg_bot
from redis_cache.auth_headers import get_auth_headers_by_telegram_id_in_message
from test_config import settings


def get_user_habits(message: Message) -> requests.Response | None:
    headers = get_auth_headers_by_telegram_id_in_message(message)
    response = requests.get(
        "{url}/api/habits/me".format(
            url=settings.api.url,
        ),
        headers=headers,
    )

    if response.status_code == HTTP_200_OK:
        habits = response.json()
        return habits
    elif response.status_code == HTTP_401_UNAUTHORIZED:
        return
    else:
        tg_bot.send_message(message.chat.id, "❌ Ошибка сервера. Попробуйте позже.")
        return
