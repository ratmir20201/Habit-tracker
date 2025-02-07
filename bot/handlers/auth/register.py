import requests

from main import tg_bot
from test_config import settings
from validators.register_validator import validate_user_data


def register(message, username: str, email: str, password: str):

    user_data = {
        "telegram_id": message.from_user.id,
        "username": username,
        "email": email,
        "password": password,
    }

    valid_user_data = validate_user_data(message, user_data)
    if valid_user_data is None:
        return

    response = requests.post(
        "{url}/auth/register".format(url=settings.api.url),
        json=valid_user_data.model_dump(),
    )

    if response.status_code == 201:
        tg_bot.send_message(
            message.chat.id,
            "✅ Регистрация успешна! Теперь отправьте команду /start для входа.",
        )
    elif response.status_code == 400:
        from handlers import get_username

        tg_bot.send_message(
            message.chat.id,
            "Пользователь с таким именем или email уже существует.",
        )
        tg_bot.send_message(
            message.chat.id, "🔁 Попробуйте еще раз.\n\nВведите ваше имя:"
        )
        tg_bot.register_next_step_handler(message, get_username)
    else:
        tg_bot.send_message(message.chat.id, "❌ Ошибка регистрации. Попробуйте снова.")
