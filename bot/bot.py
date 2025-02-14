from config import settings
from constants.all_commands import ALL_COMMANDS
from telebot import TeleBot
from telebot.types import BotCommand

tg_bot = TeleBot(settings.tg_bot.token)

tg_bot.set_my_commands(
    [BotCommand(command, description) for command, description in ALL_COMMANDS]
)


from handlers import *  # noqa
