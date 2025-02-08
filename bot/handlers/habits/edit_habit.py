from typing import Any

import requests
from helpers.habits import HabitsHelper
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from bot.main import tg_bot


@tg_bot.message_handler(commands=["edit_habit"])
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
        "Выберите привычку, которую хотите отредактировать:",
        reply_markup=keyboard,
    )
    tg_bot.register_next_step_handler(message, get_new_habit_name, habits)


def get_new_habit_name(message: Message, habits: list[dict[str, Any]]):
    """Функция для получения нового названия привычки."""
    habit_name = message.text.strip().capitalize()
    habit_object = None

    for habit in habits:
        if habit_name == habit["name"]:
            habit_object = habit
            break

    if not habit_object:
        tg_bot.send_message(message.chat.id, "❌ Такой привычки нет в вашем списке.")
        return

    tg_bot.send_message(message.chat.id, "Введите новое название для привычки:")
    tg_bot.register_next_step_handler(message, save_new_habit_name, habit_object["id"])


def save_new_habit_name(message: Message, habit_id: int):
    """Функция для сохранения нового названия привычки."""
    habits_helper = HabitsHelper(message)
    habit = habits_helper.update_habit(habit_id)

    tg_bot.send_message(
        message.chat.id,
        "✅ Привычка успешно обновлена на: {}.".format(habit["name"]),
    )
