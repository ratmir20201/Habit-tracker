from typing import Callable, cast

from message_generators.keyboards.reply.default import help_button
from message_generators.responses.default_commands import generate_help_message
from telebot.types import Message

from bot import tg_bot


@cast(Callable[[Message], None], tg_bot.message_handler(commands=["help"]))
def help_by_command(message: Message):
    """Выполнить команду help."""
    help_message(message)


@cast(
    Callable[[Message], None],
    tg_bot.message_handler(func=lambda message: message.text == help_button),
)
def help_by_keyboard(message: Message):
    """Выполнить команду help с помощью кнопки."""
    help_message(message)


def help_message(message: Message):
    """Отправляет все команды бота."""
    tg_bot.send_message(
        message.chat.id,
        generate_help_message(),
        parse_mode="Markdown",
    )
