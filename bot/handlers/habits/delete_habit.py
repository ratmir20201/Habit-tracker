from typing import Callable, cast

from helpers.habits import HabitsHelper
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.keyboards.reply.habits import delete_habit_button
from message_generators.responses.habits import generate_delete_habit_message
from message_generators.services.habits import answer_habit_delete_message
from schemas.habit import HabitSchema
from telebot.types import Message
from utils.get_habit_by_name import (
    get_habit_object_from_habits_by_name,
    take_habit_name_from_user,
)

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["deletehabit"]))
def delete_habit_by_keyboard_command(message: Message):
    """
    Выполнить команду deletehabit.

    Запрашиваем у пользователя привычку из его списка.
    """
    take_habit_name_from_user(
        message=message,
        message_text=answer_habit_delete_message,
        next_step_handler=delete_habit,
    )


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == delete_habit_button),
)
def delete_habit_by_keyboard(message: Message):
    """
    Выполнить команду deletehabit с помощью кнопки.

    Запрашиваем у пользователя привычку из его списка.
    """
    take_habit_name_from_user(
        message=message,
        message_text=answer_habit_delete_message,
        next_step_handler=delete_habit,
    )


def delete_habit(message: Message, habits: list[HabitSchema]) -> None:
    """Удаляет выбранную привычку."""
    habit_object = get_habit_object_from_habits_by_name(message, habits)

    if not habit_object:
        return

    habits_helper = HabitsHelper(message)
    habits_helper.delete_habit(habit_object.id)

    tg_bot.send_message(
        message.chat.id,
        generate_delete_habit_message(habit_name=habit_object.name),
        reply_markup=get_habits_crud_keyboard(),
        parse_mode="Markdown",
    )
