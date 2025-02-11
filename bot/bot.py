from config import settings
from telebot import TeleBot

tg_bot = TeleBot(settings.tg_bot.token)

from handlers import *  # noqa
