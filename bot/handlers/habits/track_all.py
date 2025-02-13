from helpers.habit_tracking import HabitTrackingHelper
from helpers.habits import HabitsHelper
from keyboards.inline.confirmation_tracking import get_confirmation_tracking_keyboard
from keyboards.reply.habits import get_habits_crud_keyboard
from message_generators.keyboards.reply.habits import track_all_habit_button
from message_generators.responses.congratulations import (
    generate_congratulations_message,
)
from message_generators.responses.tracking import (
    habit_already_pointed_message,
    generate_is_tracked,
)
from message_generators.services.tracking import generate_answer_track_message
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["trackall"])
def track_all_by_command(message: Message):
    add_habits_tracking(message)


@tg_bot.message_handler(func=lambda message: message.text == track_all_habit_button)
def track_all_by_keyboard(message: Message):
    add_habits_tracking(message)


def add_habits_tracking(message: Message):
    """Отправляем пользователю все его привычки для отметки."""

    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()
    if not habits:
        return

    for habit in habits:
        tg_bot.send_message(
            message.chat.id,
            generate_answer_track_message(habit_name=habit["name"]),
            reply_markup=get_confirmation_tracking_keyboard(habit["id"]),
            parse_mode="Markdown",
        )


@tg_bot.callback_query_handler(
    func=lambda call: call.data.startswith("confirm_yes")
    or call.data.startswith("confirm_no")
)
def handle_confirmation(call):
    action, habit_id = call.data.rsplit("_", 1)
    habit_id = int(habit_id)
    if action == "confirm_yes":
        habit_tracking_helper = HabitTrackingHelper(call)
        my_response, habit = habit_tracking_helper.add_tracking(habit_id=habit_id)

        if my_response == "habit_pointed":
            message_text = generate_is_tracked(
                habit_name=habit["name"],
                habit_streak=habit["streak"],
            )
        elif my_response == "habit_totally_complete":
            message_text = generate_congratulations_message(habit_name=habit["name"])
        else:
            message_text = habit_already_pointed_message

        tg_bot.send_message(
            call.message.chat.id,
            message_text,
            reply_markup=get_habits_crud_keyboard(),
            parse_mode="Markdown",
        )
    # Удаляем кнопки после выбора
    tg_bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None,
    )
