import requests

from handlers.auth.before_register import get_username
from main import tg_bot
from redis_cache.client import get_redis_client
from telebot.types import Message
from test_config import settings


@tg_bot.message_handler(commands=["start"])
def start_message(message: Message):
    telegram_id = message.from_user.id

    response = requests.post(
        "{url}/auth/telegram/login".format(url=settings.api.url),
        params={"telegram_id": telegram_id},
    )

    if response.status_code == 200:
        redis_client = get_redis_client()
        token = response.json()["token"]["access_token"]
        redis_client.setex(
            name="user_token:{telegram_id}".format(telegram_id=telegram_id),
            time=settings.redis.token_expire,
            value=token,
        )
        tg_bot.send_message(message.chat.id, "✅ Авторизация успешна!")
    elif response.status_code == 404:
        tg_bot.send_message(
            message.chat.id,
            "🔹 Вас нет в системе. Давайте зарегистрируемся!\n\nВведите ваше имя: ",
        )
        tg_bot.register_next_step_handler(message, get_username)
    else:
        tg_bot.send_message(message.chat.id, "❌ Ошибка сервера. Попробуйте позже.")
