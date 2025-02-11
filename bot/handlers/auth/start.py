from handlers.auth.before_register import get_username
from helpers.auth import AuthenticationHelper
from message_generators.responses.auth import auth_success_message
from message_generators.services.auth import register_suggestion_message
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["start"])
def start_message(message: Message):
    auth_helper = AuthenticationHelper(message)
    status_code = auth_helper.login_and_save_token_in_redis()

    if status_code == HTTP_200_OK:
        tg_bot.send_message(
            message.chat.id,
            auth_success_message,
        )
    elif status_code == HTTP_404_NOT_FOUND:
        tg_bot.send_message(
            message.chat.id,
            register_suggestion_message,
        )
        tg_bot.register_next_step_handler(message, get_username)
