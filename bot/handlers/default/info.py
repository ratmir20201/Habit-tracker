from typing import Callable, cast

from message_generators.keyboards.reply.default import info_button
from message_generators.responses.default_commands import info_message
from telebot.types import Message

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["info"]))
def info_by_command(message: Message):
    bot_info(message)


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == info_button),
)
def info_by_keyboard(message: Message):
    bot_info(message)


def bot_info(message: Message):
    tg_bot.send_message(message.chat.id, info_message)
