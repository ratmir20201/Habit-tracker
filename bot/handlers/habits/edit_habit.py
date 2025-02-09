from typing import Any

import requests
from helpers.habits import HabitsHelper
from keyboards.reply.choice_habit import get_habits_keyboard
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup
from utils.get_habit_by_name import get_habit_object_from_habits_by_name

from bot.main import tg_bot


@tg_bot.message_handler(commands=["edit_habit"])
def get_habit_name_what_we_update(message: Message):
    """Запрашиваем у пользователя название привычки."""
    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()
    if not habits:
        return

    keyboard = get_habits_keyboard(habits)

    tg_bot.send_message(
        message.chat.id,
        "Выберите привычку, которую хотите отредактировать:",
        reply_markup=keyboard,
    )
    tg_bot.register_next_step_handler(message, get_new_habit_name, habits)


def get_new_habit_name(message: Message, habits: list[dict[str, Any]]):
    """Функция для получения нового названия привычки."""
    habit_object = get_habit_object_from_habits_by_name(message, habits)

    if not habit_object:
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
