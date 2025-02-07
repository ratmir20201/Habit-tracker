import requests

from handlers.auth.before_register import get_username
from main import tg_bot
from test_config import settings


@tg_bot.message_handler(commands=["start"])
def start_message(message):
    telegram_id = message.from_user.id

    response = requests.post(
        "{url}/auth/telegram/login".format(url=settings.api.url),
        params={"telegram_id": telegram_id},
    )

    if response.status_code == 200:
        token = response.json()["token"]["access_token"]
        tg_bot.send_message(
            message.chat.id,
            "✅ Авторизация успешна! Ваш токен:\n`{token}`".format(token=token),
            parse_mode="Markdown",
        )
    elif response.status_code == 404:
        tg_bot.send_message(
            message.chat.id,
            "🔹 Вас нет в системе. Давайте зарегистрируемся!\n\nВведите ваше имя: ",
        )
        tg_bot.register_next_step_handler(message, get_username)
    else:
        tg_bot.send_message(message.chat.id, "❌ Ошибка сервера. Попробуйте позже.")
