from typing import Callable, cast

from helpers.habit_tracking import HabitTrackingHelper
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.keyboards.reply.habits import track_one_habit_button
from message_generators.services.tracking import (
    answer_point_habit_message,
    generate_tracking_message_text,
)
from schemas.habit import HabitSchema
from telebot.types import Message
from utils.get_habit_by_name import (
    get_habit_object_from_habits_by_name,
    take_habit_name_from_user,
)

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["trackone"]))
def track_one_by_command(message: Message):
    take_habit_name_from_user(
        message=message,
        message_text=answer_point_habit_message,
        next_step_handler=add_habit_tracking,
    )


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == track_one_habit_button),
)
def track_one_by_keyboard(message: Message) -> None:
    take_habit_name_from_user(
        message=message,
        message_text=answer_point_habit_message,
        next_step_handler=add_habit_tracking,
    )


def add_habit_tracking(message: Message, habits: list[HabitSchema]) -> None:
    """Обрабатываем ответ пользователя и создаем привычку."""
    habit_tracking_helper = HabitTrackingHelper(message)

    habit_object = get_habit_object_from_habits_by_name(message, habits)
    if not habit_object:
        return

    my_response, habit = habit_tracking_helper.add_tracking(habit_object.id)

    if not my_response:
        return

    message_text = generate_tracking_message_text(
        my_response=my_response,
        habit=habit,
    )

    tg_bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=get_habits_crud_keyboard(),
        parse_mode="Markdown",
    )
