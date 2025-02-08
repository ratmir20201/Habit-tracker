from constants.all_commands import ALL_COMMANDS
from telebot.types import Message

from bot.main import tg_bot


@tg_bot.message_handler(commands=["help"])
def help_message(message: Message):
    commands = [
        "/{command} - {description}".format(
            command=command,
            description=description,
        )
        for command, description in ALL_COMMANDS
    ]
    tg_bot.send_message(message.chat.id, "\n".join(commands))
