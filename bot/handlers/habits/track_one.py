from typing import cast, Callable

from helpers.habit_tracking import (
    HabitTrackingHelper,
    HABIT_ALREADY_POINTED,
    HABIT_COMPLETED,
    HABIT_POINTED,
)
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.errors.server import unexpected_server_error_message
from message_generators.keyboards.reply.habits import track_one_habit_button
from message_generators.responses.congratulations import (
    generate_congratulations_message,
)
from message_generators.responses.tracking import (
    generate_is_tracked,
    habit_already_pointed_message,
)
from message_generators.services.tracking import answer_point_habit_message
from telebot.types import Message
from utils.get_habit_by_name import (
    get_habit_name_from_user,
    get_habit_object_from_habits_by_name,
)

from bot import tg_bot
from schemas.habit import HabitSchema


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["trackone"]))
def track_one_by_command(message: Message):
    get_habit_name_from_user(
        message=message,
        message_text=answer_point_habit_message,
        next_step_handler=add_habit_tracking,
    )


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == track_one_habit_button),
)
def track_one_by_keyboard(message: Message) -> None:
    get_habit_name_from_user(
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

    if (my_response == HABIT_POINTED) and (habit is not None):
        message_text = generate_is_tracked(
            habit_name=habit.name,
            habit_streak=habit.streak,
        )
    elif (my_response == HABIT_COMPLETED) and (habit is not None):
        message_text = generate_congratulations_message(habit_name=habit.name)
    elif my_response == HABIT_ALREADY_POINTED:
        message_text = habit_already_pointed_message
    else:
        message_text = unexpected_server_error_message

    tg_bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=get_habits_crud_keyboard(),
        parse_mode="Markdown",
    )
