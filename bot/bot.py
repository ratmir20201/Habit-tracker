import asyncio

from config import settings
from constants.all_commands import ALL_COMMANDS
from telebot import TeleBot, logger
from telebot.types import BotCommand

tg_bot = TeleBot(settings.tg_bot.token)

tg_bot.set_my_commands(
    [BotCommand(command, description) for command, description in ALL_COMMANDS]
)


async def set_webhook() -> None:
    """Удаляет старый вебхук и устанавливает новый."""
    tg_bot.delete_webhook(drop_pending_updates=True)

    await asyncio.sleep(1)

    tg_bot.set_webhook(url=settings.tg_bot.webhook_url)
    logger.info("Бот успешно установил Webhook!")


import handlers  # noqa: E402, F401
