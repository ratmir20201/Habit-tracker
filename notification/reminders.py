from datetime import datetime

from config import settings
from generate_message import generate_reminder_message
from helpers.untrack import UntrackedUsers
from logger import logger

from bot import tg_bot


async def send_reminders():
    """Функция для отправки оповещения пользователю о его привычках."""

    api_helper = UntrackedUsers()
    await api_helper.init()
    untracked_users = await api_helper.get_untracked_users()

    if not untracked_users:
        logger.info("Не надо делать оповещения.")
        return

    for i_user_habits in untracked_users:
        tg_bot.send_message(
            i_user_habits["telegram_id"],
            await generate_reminder_message(i_user_habits["habits"]),
            parse_mode="Markdown",
        )
