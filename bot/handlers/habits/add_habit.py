from telebot.types import Message

from bot.main import tg_bot
from helpers.habits import HabitsHelper
from message_generators.responses.habits import generate_add_habit_message
from message_generators.services.habits import answer_habit_name_message


@tg_bot.message_handler(commands=["addhabit"])
def get_data_for_habit(message: Message):
    """Запрашиваем у пользователя название привычки."""
    tg_bot.send_message(message.chat.id, answer_habit_name_message)
    habit_data = tg_bot.register_next_step_handler(message, add_habit)


def add_habit(message: Message):
    """Обрабатываем ответ пользователя и создаем привычку."""
    habits_helper = HabitsHelper(message)
    habit = habits_helper.add_habit()

    message_text = generate_add_habit_message(habit_name=habit["name"])

    tg_bot.send_message(
        message.chat.id,
        message_text,
        parse_mode="Markdown",
    )
