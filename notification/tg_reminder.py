from typing import Any

from generate_message import generate_reminder_message

from .bot import tg_bot


async def send_reminders(untracked_user_habits: dict[str, Any]) -> None:
    """Функция для отправки оповещения пользователю о его привычках."""

    tg_bot.send_message(
        untracked_user_habits["telegram_id"],
        await generate_reminder_message(untracked_user_habits["habits"]),
        parse_mode="Markdown",
    )
