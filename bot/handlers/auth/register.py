import requests

from main import tg_bot
from test_config import settings


def register_user(message):
    telegram_id = message.from_user.id
    username = message.text
    email = message.text
    password = message.text

    data = {
        "telegram_id": telegram_id,
        "username": username,
        "email": email,
        "password": password,
    }
    response = requests.post(
        "{url}/auth/register".format(url=settings.api.url),
        json=data,
    )

    if response.status_code == 201:
        tg_bot.send_message(
            message.chat.id,
            "✅ Регистрация успешна! Теперь отправьте команду /start для входа.",
        )
    else:
        tg_bot.send_message(message.chat.id, "❌ Ошибка регистрации. Попробуйте снова.")
