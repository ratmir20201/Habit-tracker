from typing import Any

from helpers.habits import HabitsHelper
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.keyboards.reply.habits import get_habits_button
from message_generators.responses.habits import generate_get_habits_message
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["gethabits"])
def get_habits_by_command(message: Message):
    get_habits(message)


@tg_bot.message_handler(func=lambda message: message.text == get_habits_button)
def get_habits_by_keyboard(message: Message):
    get_habits(message)


def get_habits(message: Message) -> None:
    """Команда для отображения всех привычек пользователя."""

    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    message_text = generate_get_habits_message(habits=habits)
    tg_bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=get_habits_crud_keyboard(),
        parse_mode="Markdown",
    )
