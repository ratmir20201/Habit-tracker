from typing import Any

from exceptions.validate_register_data_handler import invalid_user_data_handler
from message_generators.errors.auth import generate_register_error_message
from message_generators.services.auth import try_again_register_message
from pydantic import ValidationError
from schemas.exceptions import InvalidUserDataError
from schemas.register import RegisterSchema
from telebot.types import Message

from bot import tg_bot


@invalid_user_data_handler
def validate_user_data(
    message: Message,
    user_data: dict[str, Any],
) -> RegisterSchema:

    try:
        valid_user_data = RegisterSchema.model_validate(user_data)
        return valid_user_data
    except ValidationError as exc:
        from handlers.auth.before_register import take_username_for_register

        errors = exc.errors()
        error_message = generate_register_error_message(errors=errors)
        tg_bot.send_message(message.chat.id, error_message)

        tg_bot.send_message(message.chat.id, try_again_register_message)
        tg_bot.register_next_step_handler(message, take_username_for_register)

        raise InvalidUserDataError("Ошибка валидации данных пользователя")
