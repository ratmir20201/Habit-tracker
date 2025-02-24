from typing import cast, Callable

from keyboards.reply.start import get_start_keyboard
from message_generators.keyboards.reply.default import start_button
from message_generators.responses.default_commands import hello_message
from telebot.types import Message

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["start", "hello"]))
def hello_by_command(message: Message):
    hello(message)


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == start_button),
)
def hello_by_keyboard(message: Message):
    hello(message)


def hello(message: Message):
    tg_bot.send_message(
        message.chat.id,
        hello_message,
        reply_markup=get_start_keyboard(),
    )
