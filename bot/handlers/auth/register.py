from helpers.auth import AuthenticationHelper
from message_generators.errors.auth import user_already_exist_message
from message_generators.responses.auth import register_success_message
from message_generators.services.auth import (input_name_message,
                                              try_again_register_message)
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["register"])
def register_new_user(message: Message):
    from handlers import get_username

    tg_bot.send_message(message.chat.id, input_name_message)
    tg_bot.register_next_step_handler(message, get_username)


def register(message: Message, username: str, email: str, password: str):
    user_data = {
        "telegram_id": message.from_user.id,
        "username": username,
        "email": email,
        "password": password,
    }

    auth_helper = AuthenticationHelper(message)
    my_response = auth_helper.register_user(user_data=user_data)

    if my_response == "success":
        tg_bot.send_message(
            message.chat.id,
            register_success_message,
        )
    elif my_response == "register_user_already_exist":
        from handlers import get_username

        tg_bot.send_message(
            message.chat.id,
            user_already_exist_message,
        )
        tg_bot.send_message(
            message.chat.id,
            try_again_register_message,
        )
        tg_bot.register_next_step_handler(message, get_username)
