import requests

from telebot.types import Message
from bot.main import tg_bot
from redis_cache.auth_headers import get_auth_headers_by_telegram_id_in_message
from test_config import settings


@tg_bot.message_handler(commands=["get_habits"])
def get_habits(message: Message):
    """Команда для отображения всех привычек пользователя."""

    headers = get_auth_headers_by_telegram_id_in_message(message)
    response = requests.get(
        "{url}/api/habits/me".format(url=settings.api.url),
        headers=headers,
    )
    if response.status_code == 200:
        habits = response.json()
        message_text = "✨ *Ваши привычки:*\n\n"

        for habit in habits:
            habit_name = habit["name"].capitalize()
            message_text += "📌 *{habit_name}*\n".format(habit_name=habit_name)
            # message_text += "   🔥 Дней подряд: *{habit_streak}*"
        tg_bot.send_message(
            message.chat.id,
            message_text,
            parse_mode="Markdown",
        )
    else:
        tg_bot.send_message(message.chat.id, "❌ Ошибка сервера. Попробуйте позже.")
