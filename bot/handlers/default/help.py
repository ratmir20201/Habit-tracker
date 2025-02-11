from message_generators.responses.default_commands import generate_help_message
from telebot.types import Message

from bot.main import tg_bot


@tg_bot.message_handler(commands=["help"])
def help_message(message: Message):

    tg_bot.send_message(
        message.chat.id,
        generate_help_message(),
        parse_mode="Markdown",
    )
