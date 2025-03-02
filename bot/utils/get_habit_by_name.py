from typing import Callable

from helpers.habits import HabitsHelper
from keyboards.reply.choice_habit import get_habits_keyboard
from message_generators.errors.habits import (
    habit_not_exist_message,
    habits_not_exist_message,
)
from schemas.habit import HabitSchema
from telebot.types import Message

from bot import tg_bot


def get_habit_object_from_habits_by_name(
    message: Message,
    habits: list[HabitSchema],
) -> HabitSchema | None:
    """Отдает объект привычки из списка привычек пользователя."""

    habit_name = message.text.strip().capitalize()
    habit_object = None

    for habit in habits:
        if habit_name == habit.name:
            habit_object = habit
            break

    if not habit_object:
        tg_bot.send_message(
            message.chat.id,
            habit_not_exist_message,
        )
        return None

    return habit_object


def take_habit_name_from_user(
    message: Message,
    message_text: str,
    next_step_handler: Callable[[Message, list[HabitSchema]], None],
) -> None:
    """Запрашиваем у пользователя название привычки."""

    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    if not habits:
        tg_bot.send_message(message.chat.id, habits_not_exist_message)
        return

    keyboard = get_habits_keyboard(habits)

    tg_bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=keyboard,
    )
    tg_bot.register_next_step_handler(message, next_step_handler, habits)
