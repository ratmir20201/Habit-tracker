from typing import Any

from helpers.habit_tracking import HabitTrackingHelper
from helpers.habits import HabitsHelper
from keyboards.inline.confirmation_tracking import get_confirmation_tracking_keyboard
from telebot.types import Message

from bot.main import tg_bot


@tg_bot.message_handler(commands=["trackall"])
def add_habits_tracking(message: Message):
    """Запрашиваем у пользователя название привычки."""
    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()
    if not habits:
        return

    for habit in habits:
        tg_bot.send_message(
            message.chat.id,
            "Выполнили ли вы сегодня привычку  *{}*?".format(habit["name"]),
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
        my_response, habit_name = habit_tracking_helper.add_tracking(habit_id=habit_id)

        if my_response == "habit_not_pointed":
            tg_bot.send_message(
                call.message.chat.id,
                "Данная привычка уже отмечена как выполненная сегодня!",
            )
        elif my_response == "habit_totally_complete":
            tg_bot.send_message(
                call.message.chat.id,
                "🎉 Поздравляем! Вы успешно закрепили привычку {habit_name}, выполнив её {habit_streak} дней подряд. "
                "Теперь она стала частью вашей жизни!".format(
                    habit_name=habit_name,
                    habit_streak=settings.tg_bot.carry_over_complete_habits_days,
                ),
            )

    # Удаляем кнопки после выбора
    tg_bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None,
    )
