from telebot.types import Message

from main import tg_bot


def is_command(message: Message) -> bool:
    if message.text.startswith("/"):
        tg_bot.send_message(message.chat.id, "❌ Регистрация отменена.")
        return True
    return False
