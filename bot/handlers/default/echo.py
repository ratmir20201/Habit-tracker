from message_generators.responses.default_commands import echo_message
from telebot.types import Message

from bot.main import tg_bot


@tg_bot.message_handler(func=lambda message: True)
def echo(message: Message):
    tg_bot.reply_to(message, echo_message)
