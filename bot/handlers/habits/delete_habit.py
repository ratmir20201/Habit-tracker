from typing import cast, Callable

from helpers.habits import HabitsHelper
from keyboards.reply.choice_habit import get_habits_keyboard
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.errors.habits import habits_not_exist_message
from message_generators.keyboards.reply.habits import delete_habit_button
from message_generators.responses.habits import generate_delete_habit_message
from message_generators.services.habits import answer_habit_delete_message
from telebot.types import Message
from utils.get_habit_by_name import (
    get_habit_name_from_user,
    get_habit_object_from_habits_by_name,
)

from bot import tg_bot
from schemas.habit import HabitSchema


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["deletehabit"]))
def delete_habit_by_keyboard_command(message: Message):
    get_habit_name_from_user(
        message=message,
        message_text=answer_habit_delete_message,
        next_step_handler=delete_habit,
    )


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == delete_habit_button),
)
def delete_habit_by_keyboard(message: Message):
    get_habit_name_from_user(
        message=message,
        message_text=answer_habit_delete_message,
        next_step_handler=delete_habit,
    )


def delete_habit(message: Message, habits: list[HabitSchema]) -> None:
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
