from message_generators.errors.auth import generate_register_error_message
from message_generators.services.auth import try_again_register_message
from pydantic import ValidationError
from schemas.register import RegisterSchema

from main import tg_bot


def validate_user_data(message, data) -> RegisterSchema | None:

    try:
        user_data = RegisterSchema(**data)
        return user_data
    except ValidationError as e:
        from handlers import get_username

        errors = e.errors()
        error_message = generate_register_error_message(errors=errors)
        tg_bot.send_message(message.chat.id, error_message)

        tg_bot.send_message(message.chat.id, try_again_register_message)
        tg_bot.register_next_step_handler(message, get_username)
        return None
