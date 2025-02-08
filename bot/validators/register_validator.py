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
        for error in errors:
            field = error["loc"][0]
            error_message = error["msg"]

            if field == "email":
                error_message = (
                    "Некорректный формат email. Пожалуйста, введите правильный email."
                )
            elif field == "password":
                error_message = "Пароль должен содержать минимум 8 символов, одну заглавную букву и цифру."
            tg_bot.send_message(message.chat.id, "❌ Ошибка: {}".format(error_message))

        tg_bot.send_message(
            message.chat.id, "🔁 Попробуйте еще раз.\n\nВведите ваше имя:"
        )
        tg_bot.register_next_step_handler(message, get_username)
        return None
