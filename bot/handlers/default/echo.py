from typing import Callable, cast

from message_generators.responses.default_commands import echo_message
from telebot.types import Message

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(func=lambda message: True))
def echo(message: Message):
    tg_bot.reply_to(message, echo_message)
