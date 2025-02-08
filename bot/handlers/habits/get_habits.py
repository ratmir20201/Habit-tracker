import requests
from helpers.habits import HabitsHelper
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from telebot.types import Message

from bot.main import tg_bot


@tg_bot.message_handler(commands=["get_habits"])
def get_habits(message: Message):
    """Команда для отображения всех привычек пользователя."""
    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    message_text = "✨ *Ваши привычки:*\n\n"

    for habit in habits:
        message_text += "📌 *{habit_name}*\n".format(habit_name=habit["name"])
        # message_text += "   🔥 Дней подряд: *{habit_streak}*"
    tg_bot.send_message(
        message.chat.id,
        message_text,
        parse_mode="Markdown",
    )
