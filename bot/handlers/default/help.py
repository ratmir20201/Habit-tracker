from message_generators.keyboards.reply.default import help_button
from message_generators.responses.default_commands import generate_help_message
from telebot.types import Message

from bot import tg_bot


@tg_bot.message_handler(commands=["help"])
def help_by_command(message: Message):
    help_message(message)


@tg_bot.message_handler(func=lambda message: message.text == help_button)
def help_by_keyboard(message: Message):
    help_message(message)


def help_message(message: Message):
    tg_bot.send_message(
        message.chat.id,
        generate_help_message(),
        parse_mode="Markdown",
    )
