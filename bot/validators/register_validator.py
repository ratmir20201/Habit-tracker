from typing import Any

from telebot.types import Message

from exceptions.validate_register_data_handler import invalid_user_data_handler
from message_generators.errors.auth import generate_register_error_message
from message_generators.services.auth import try_again_register_message
from pydantic import ValidationError
from schemas.register import RegisterSchema

from bot import tg_bot
from schemas.exceptions import InvalidUserDataError


@invalid_user_data_handler
def validate_user_data(
    message: Message,
    data: dict[str, Any],
) -> RegisterSchema:

    try:
        user_data = RegisterSchema(**data)
        return user_data
    except ValidationError as e:
        from handlers.auth.before_register import get_username

        errors = e.errors()
        error_message = generate_register_error_message(errors=errors)
        tg_bot.send_message(message.chat.id, error_message)

        tg_bot.send_message(message.chat.id, try_again_register_message)
        tg_bot.register_next_step_handler(message, get_username)

        raise InvalidUserDataError("Ошибка валидации данных пользователя")
