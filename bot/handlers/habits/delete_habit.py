from typing import Any

import requests
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.main import tg_bot
from utils.habits import HabitsHelper


@tg_bot.message_handler(commands=["delete_habit"])
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
    tg_bot.register_next_step_handler(message, get_habit_id, habits)


def get_habit_id(message: Message, habits: list[dict[str, Any]]):
    """Команда для изменения привычки."""
    habit_name = message.text.strip().capitalize()
    habit_object = None

    for habit in habits:
        if habit_name == habit["name"]:
            habit_object = habit
            break

    delete_habit(message, habit_object)


def delete_habit(message: Message, habit_object: dict[str, Any]):
    habits_helper = HabitsHelper(message)
    habits_helper.delete_habit(habit_object["id"])

    tg_bot.send_message(
        message.chat.id,
        "✅ Привычка {} успешно удалена.".format(habit_object["name"]),
    )
