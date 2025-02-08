from telebot.types import Message

from bot.main import tg_bot


@tg_bot.message_handler(commands=["hello"])
def hello_message(message: Message):
    tg_bot.reply_to(message, "Привет! Я Telegram-бот с FastAPI!")
