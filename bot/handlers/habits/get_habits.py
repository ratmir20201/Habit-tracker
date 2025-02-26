from typing import Callable, cast

from helpers.habits import HabitsHelper
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.errors.habits import habits_not_exist_message
from message_generators.keyboards.reply.habits import get_habits_button
from message_generators.responses.habits import generate_get_habits_message
from telebot.types import Message

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["gethabits"]))
def command_get_habits(message: Message):
    send_habits(message)


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == get_habits_button),
)
def keyboard_get_habits(message: Message):
    send_habits(message)


def send_habits(message: Message) -> None:
    """Команда для отображения всех привычек пользователя."""

    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    if not habits:
        tg_bot.send_message(message.chat.id, habits_not_exist_message)
        return

    message_text = generate_get_habits_message(habits=habits)
    tg_bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=get_habits_crud_keyboard(),
        parse_mode="Markdown",
    )
