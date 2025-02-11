from typing import Any

from helpers.habit_tracking import HabitTrackingHelper
from helpers.habits import HabitsHelper
from keyboards.reply.choice_habit import get_habits_keyboard
from telebot.types import Message

from test_config import settings
from utils.get_habit_by_name import get_habit_object_from_habits_by_name

from bot.main import tg_bot


@tg_bot.message_handler(commands=["trackone"])
def get_habit_name(message: Message):
    """Запрашиваем у пользователя название привычки."""
    habits_helper = HabitsHelper(message)
    habits = habits_helper.get_user_habits()
    if not habits:
        return

    keyboard = get_habits_keyboard(habits)

    tg_bot.send_message(
        message.chat.id,
        "Выберите привычку, которую хотите пометить как выполненную:",
        reply_markup=keyboard,
    )
    tg_bot.register_next_step_handler(message, add_habit_tracking, habits)


def add_habit_tracking(message: Message, habits: list[dict[str, Any]]):
    """Обрабатываем ответ пользователя и создаем привычку."""
    habit_tracking_helper = HabitTrackingHelper(message)

    habit_object = get_habit_object_from_habits_by_name(message, habits)
    habit_name = habit_object["name"]
    if not habit_object:
        return

    my_response, habit_name = habit_tracking_helper.add_tracking(habit_object["id"])

    if my_response == "habit_pointed":
        message_text = (
            "✅ Привычка *{habit_name}* успешно помечена как выполненная!".format(
                habit_name=habit_name,
            )
        )

        tg_bot.send_message(message.chat.id, message_text, parse_mode="Markdown")
    elif my_response == "habit_totally_complete":
        tg_bot.send_message(
            message.chat.id,
            "🎉 Поздравляем! Вы успешно закрепили привычку {habit_name}, выполнив её {habit_streak} дней подряд. "
            "Теперь она стала частью вашей жизни!".format(
                habit_name=habit_name,
                habit_streak=settings.tg_bot.carry_over_complete_habits_days,
            ),
        )
    else:
        tg_bot.send_message(
            message.chat.id,
            "Привычка уже отмечена как выполненная сегодня!",
        )
