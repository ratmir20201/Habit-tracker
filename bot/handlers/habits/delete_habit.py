from typing import Any

from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from bot.main import tg_bot
from helpers.habits import HabitsHelper
from message_generators.errors.habits import habits_not_exist_message
from message_generators.responses.habits import generate_delete_habit_message
from message_generators.services.habits import answer_habit_delete_message
from utils.get_habit_by_name import get_habit_object_from_habits_by_name


@tg_bot.message_handler(commands=["deletehabit"])
def get_habit_name_what_we_update(message: Message):
    """Запрашиваем у пользователя название привычки."""
    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    if not habits:
        tg_bot.send_message(message.chat.id, habits_not_exist_message)
        return

    # Создаем клавиатуру с привычками
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for habit in habits:
        keyboard.add(KeyboardButton(habit["name"]))

    tg_bot.send_message(
        message.chat.id,
        answer_habit_delete_message,
        reply_markup=keyboard,
    )
    tg_bot.register_next_step_handler(message, delete_habit, habits)


def delete_habit(message: Message, habits: list[dict[str, Any]]):
    habit_object = get_habit_object_from_habits_by_name(message, habits)

    habits_helper = HabitsHelper(message)
    habits_helper.delete_habit(habit_object["id"])

    tg_bot.send_message(
        message.chat.id,
        generate_delete_habit_message(habit_name=habit_object["name"]),
        parse_mode="Markdown",
    )
