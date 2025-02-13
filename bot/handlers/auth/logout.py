from helpers.auth import AuthenticationHelper
from message_generators.keyboards.reply.default import logout_button
from message_generators.responses.auth import (
    already_logout_message,
    logout_success_message,
)
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["logout"])
def logout_by_command(message: Message):
    logout(message)


@tg_bot.message_handler(func=lambda message: message.text == logout_button)
def logout_by_keyboard(message: Message):
    logout(message)


def logout(message: Message):
    auth_helper = AuthenticationHelper(message)
    my_response = auth_helper.logout_and_delete_token_in_redis()

    if my_response == "success":
        tg_bot.send_message(message.chat.id, logout_success_message)
    elif my_response == "user_already_logout":
        tg_bot.send_message(message.chat.id, already_logout_message)
