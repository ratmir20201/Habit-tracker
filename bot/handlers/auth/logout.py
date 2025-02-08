from helpers.auth import AuthenticationHelper
from starlette.status import (HTTP_200_OK, HTTP_401_UNAUTHORIZED,
                              HTTP_404_NOT_FOUND)
from telebot.types import Message

from main import tg_bot


@tg_bot.message_handler(commands=["logout"])
def logout(message: Message):
    auth_helper = AuthenticationHelper(message)
    status_code = auth_helper.logout_and_delete_token_in_redis()

    if status_code == HTTP_200_OK:
        tg_bot.send_message(message.chat.id, "✅ Вы успешно вышли из системы!")
    elif status_code == HTTP_401_UNAUTHORIZED:
        tg_bot.send_message(message.chat.id, "⚠️ Вы уже вышли из системы.")
