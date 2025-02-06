from bot.main import tg_bot
from constants.bot_info import INFO_TEXT


@tg_bot.message_handler(commands=["info"])
def get_info(message):
    tg_bot.reply_to(message, INFO_TEXT)
