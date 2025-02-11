from typing import Any

from message_generators.errors.habits import habit_not_exist_message
from telebot.types import Message

from bot import tg_bot


def get_habit_object_from_habits_by_name(
    message: Message,
    habits: list[dict[str, Any]],
) -> dict[str, Any] | None:
    habit_name = message.text.strip().capitalize()
    habit_object = None

    for habit in habits:
        if habit_name == habit["name"]:
            habit_object = habit
            break

    if not habit_object:
        tg_bot.send_message(
            message.chat.id,
            habit_not_exist_message,
        )
        return None

    return habit_object
