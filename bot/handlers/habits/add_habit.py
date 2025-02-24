from typing import Callable, cast

from helpers.habits import HabitsHelper
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.errors.habits import habit_already_exist_message
from message_generators.keyboards.reply.habits import (
    add_habit_button,
    add_first_habit_button,
)
from message_generators.responses.habits import generate_add_habit_message
from message_generators.services.habits import answer_habit_name_message
from telebot.types import Message

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["addhabit"]))
def add_habits_by_command(message: Message):
    get_habit_name(message)


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(
        func=lambda message: message.text == add_habit_button
        or message.text == add_first_habit_button
    ),
)
def add_habits_by_keyboard(message: Message):
    get_habit_name(message)


def get_habit_name(message: Message):
    """Запрашиваем у пользователя название привычки."""
    tg_bot.send_message(message.chat.id, answer_habit_name_message)
    habit_data = tg_bot.register_next_step_handler(message, add_habit)


def add_habit(message: Message):
    """Обрабатываем ответ пользователя и создаем привычку."""
    habits_helper = HabitsHelper(message)
    habit = habits_helper.add_habit()

    if not habit:
        tg_bot.send_message(
            message.chat.id,
            habit_already_exist_message,
        )
        return

    message_text = generate_add_habit_message(habit_name=habit.name)

    tg_bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=get_habits_crud_keyboard(),
        parse_mode="Markdown",
    )
