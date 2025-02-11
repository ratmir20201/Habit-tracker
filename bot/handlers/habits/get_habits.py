from helpers.habits import HabitsHelper
from message_generators.responses.habits import generate_get_habits_message
from telebot.types import Message

from bot.main import tg_bot


@tg_bot.message_handler(commands=["gethabits"])
def get_habits(message: Message):
    """Команда для отображения всех привычек пользователя."""
    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    message_text = generate_get_habits_message(habits=habits)
    tg_bot.send_message(message.chat.id, message_text, parse_mode="Markdown")
