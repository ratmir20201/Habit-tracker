from typing import Callable, cast

from helpers.habit_tracking import HabitTrackingHelper
from helpers.habits import HabitsHelper
from keyboards.inline.confirmation_tracking import \
    get_confirmation_tracking_keyboard
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.errors.habits import habits_not_exist_message
from message_generators.keyboards.reply.habits import track_all_habit_button
from message_generators.services.tracking import (
    generate_answer_track_message, generate_tracking_message_text)
from schemas.habit import HabitSchema
from telebot.types import CallbackQuery, Message

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["trackall"]))
def track_all_by_command(message: Message) -> None:
    add_habits_tracking(message)


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == track_all_habit_button),
)
def track_all_by_keyboard(message: Message) -> None:
    add_habits_tracking(message)


def add_habits_tracking(message: Message) -> None:
    """Отправляем пользователю все его привычки для отметки."""

    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()

    if not habits:
        tg_bot.send_message(message.chat.id, habits_not_exist_message)
        return

    for habit in habits:
        tg_bot.send_message(
            message.chat.id,
            generate_answer_track_message(habit_name=habit.name),
            reply_markup=get_confirmation_tracking_keyboard(habit.id),
            parse_mode="Markdown",
        )


@cast(
    Callable[[Message], None],
    tg_bot.callback_query_handler(
        func=lambda call: (call.data.startswith("confirm_yes"))
        or (call.data.startswith("confirm_no"))
    ),
)
def handle_confirmation(call: CallbackQuery) -> None:
    action, habit_id = get_action_and_habit_id(call=call)
    if action == "confirm_yes":
        habit_tracking_helper = HabitTrackingHelper(call)
        my_response, habit = habit_tracking_helper.add_tracking(habit_id=habit_id)

        if not my_response:
            return

        send_confirmation_tracking_message(
            my_response=my_response,
            habit=habit,
            message=call.message,
        )

    delete_buttons(call=call)


def delete_buttons(call: CallbackQuery) -> None:
    """Удаляет кнопки после выбора"""
    tg_bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None,
    )


def get_action_and_habit_id(call: CallbackQuery) -> tuple[str, int]:
    action, habit_id = call.data.rsplit("_", 1)
    habit_id = int(habit_id)

    return action, habit_id


def send_confirmation_tracking_message(
    my_response: str,
    habit: HabitSchema | None,
    message: Message,
) -> None:
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
