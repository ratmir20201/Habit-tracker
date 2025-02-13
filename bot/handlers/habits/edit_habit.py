from typing import Any

from helpers.habits import HabitsHelper
from keyboards.reply.choice_habit import get_habits_keyboard
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.keyboards.reply.habits import edit_habit_button
from message_generators.responses.habits import generate_edit_habit_message
from message_generators.services.habits import (
    answer_habit_edit_message,
    answer_new_habit_name_message,
)
from telebot.types import Message
from utils.get_habit_by_name import (
    get_habit_object_from_habits_by_name,
    get_habit_name_from_user,
)

from bot import tg_bot


@tg_bot.message_handler(commands=["edithabit"])
def edit_habit_by_command(message: Message):
    get_habit_name_from_user(
        message=message,
        message_text=answer_habit_edit_message,
        next_step_handler=get_new_habit_name,
    )


@tg_bot.message_handler(func=lambda message: message.text == edit_habit_button)
def edit_habit_by_keyboard(message: Message):
    get_habit_name_from_user(
        message=message,
        message_text=answer_habit_edit_message,
        next_step_handler=get_new_habit_name,
    )


def get_new_habit_name(message: Message, habits: list[dict[str, Any]]):
    """Функция для получения нового названия привычки."""
    habit_object = get_habit_object_from_habits_by_name(message, habits)

    if not habit_object:
        return

    tg_bot.send_message(message.chat.id, answer_new_habit_name_message)
    tg_bot.register_next_step_handler(message, save_new_habit_name, habit_object["id"])


def save_new_habit_name(message: Message, habit_id: int):
    """Функция для сохранения нового названия привычки."""
    habits_helper = HabitsHelper(message)
    habit = habits_helper.update_habit(habit_id)

    tg_bot.send_message(
        message.chat.id,
        generate_edit_habit_message(habit_name=habit["name"]),
        reply_markup=get_habits_crud_keyboard(),
        parse_mode="Markdown",
    )
