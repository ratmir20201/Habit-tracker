from typing import Callable, cast

from helpers.auth import AuthenticationHelper
from message_generators.errors.auth import (
    unexpected_register_error_message,
    user_already_exist_message,
)
from message_generators.responses.auth import register_success_message
from message_generators.services.auth import (
    input_name_message,
    try_again_register_message,
)
from telebot.types import Message
from validators.register_validator import validate_user_data

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["register"]))
def register_new_user(message: Message):
    from handlers.auth.before_register import take_username_for_register

    tg_bot.send_message(message.chat.id, input_name_message)
    tg_bot.register_next_step_handler(message, take_username_for_register)


def register(
    message: Message,
    username: str,
    email: str,
    password: str,
) -> None:
    user_data = {
        "telegram_id": message.from_user.id,
        "username": username,
        "email": email,
        "password": password,
    }

    valid_user_data = validate_user_data(message, user_data)
    if not valid_user_data:
        return

    auth_helper = AuthenticationHelper(message)
    my_response = auth_helper.register_user(user_data=valid_user_data)

    if my_response == "success":
        tg_bot.send_message(
            message.chat.id,
            register_success_message,
            parse_mode="Markdown",
        )
    elif my_response == "register_user_already_exist":
        from handlers.auth.before_register import take_username_for_register

        tg_bot.send_message(
            message.chat.id,
            user_already_exist_message,
            parse_mode="Markdown",
        )
        tg_bot.send_message(
            message.chat.id,
            try_again_register_message,
            parse_mode="Markdown",
        )
        tg_bot.register_next_step_handler(message, take_username_for_register)
    else:
        tg_bot.send_message(
            message.chat.id,
            unexpected_register_error_message,
        )
