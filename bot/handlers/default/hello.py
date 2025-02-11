from message_generators.responses.default_commands import hello_message
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["hello"])
def hello(message: Message):
    tg_bot.reply_to(message, hello_message)
