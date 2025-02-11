from typing import Any

import requests
from helpers.habits import HabitsHelper
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from bot.main import tg_bot
from utils.get_habit_by_name import get_habit_object_from_habits_by_name


@tg_bot.message_handler(commands=["deletehabit"])
def get_habit_name_what_we_update(message: Message):
    """Запрашиваем у пользователя название привычки."""
    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    if not habits:
        tg_bot.send_message(message.chat.id, "❌ У вас пока нет привычек.")
        return

    # Создаем клавиатуру с привычками
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for habit in habits:
        keyboard.add(KeyboardButton(habit["name"]))

    tg_bot.send_message(
        message.chat.id,
        "Выберите привычку, которую хотите удалить:",
        reply_markup=keyboard,
    )
    tg_bot.register_next_step_handler(message, delete_habit, habits)


def delete_habit(message: Message, habits: list[dict[str, Any]]):
    habit_object = get_habit_object_from_habits_by_name(message, habits)

    habits_helper = HabitsHelper(message)
    habits_helper.delete_habit(habit_object["id"])

    tg_bot.send_message(
        message.chat.id,
        "✅ Привычка {} успешно удалена.".format(habit_object["name"]),
    )
