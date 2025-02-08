from constants.bot_info import INFO_TEXT
from telebot.types import Message

from bot.main import tg_bot


@tg_bot.message_handler(commands=["info"])
def get_info(message: Message):
    tg_bot.reply_to(message, INFO_TEXT)
