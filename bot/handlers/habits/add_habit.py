import requests
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from telebot.types import Message
from bot.main import tg_bot
from redis_cache.auth_headers import get_auth_headers_by_telegram_id_in_message
from test_config import settings
from utils.habits import HabitsHelper


@tg_bot.message_handler(commands=["add_habit"])
def get_data_for_habit(message: Message):
    """Запрашиваем у пользователя название привычки."""
    tg_bot.send_message(message.chat.id, "Введите название привычки:")
    habit_data = tg_bot.register_next_step_handler(message, add_habit)


def add_habit(message: Message):
    """Обрабатываем ответ пользователя и создаем привычку."""
    habits_helper = HabitsHelper(message)
    habit = habits_helper.add_habit()

    habit_name = habit["name"]
    message_text = (
        "✨ *Новая привычка добавлена!* ✨\n\n"
        "✅ Привычка *{habit_name}* успешно создана!"
    ).format(
        habit_name=habit_name,
    )

    tg_bot.send_message(
        message.chat.id,
        message_text,
        parse_mode="Markdown",
    )
