from telebot.types import Message

from main import tg_bot
from redis_cache.client import get_redis_client


def get_auth_headers_by_telegram_id_in_message(
    message: Message,
) -> dict[str, str] | None:
    telegram_id = message.from_user.id
    redis_client = get_redis_client()
    token = redis_client.get("user_token:{telegram_id}".format(telegram_id=telegram_id))

    if not token:
        tg_bot.send_message(message.chat.id, "❌ Вы не авторизованы! Введите /start")
        return None

    headers = {"Authorization": "Bearer {token}".format(token=token)}

    return headers
