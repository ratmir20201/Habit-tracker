from bot.main import tg_bot


@tg_bot.message_handler(func=lambda message: True)
def echo_message(message):
    tg_bot.reply_to(message, "К сожалению я не знаю такой команды.")
