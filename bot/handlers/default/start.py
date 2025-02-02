from bot.main import tg_bot


@tg_bot.message_handler(commands=["start", "main", "hello"])
def start_message(message):
    tg_bot.reply_to(message, "Привет! Я Telegram-бот с FastAPI!")
