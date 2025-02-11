from message_generators.services.auth import register_canceled_message
from telebot.types import Message

from main import tg_bot


def is_command(message: Message) -> bool:
    if message.text.startswith("/"):
        tg_bot.send_message(message.chat.id, register_canceled_message)
        return True
    return False
