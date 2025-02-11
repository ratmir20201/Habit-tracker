from message_generators.responses.default_commands import info_message
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["info"])
def get_info(message: Message):
    tg_bot.reply_to(message, info_message)
