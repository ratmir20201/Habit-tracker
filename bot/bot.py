import asyncio

from telebot import TeleBot, apihelper

from settings.config import settings

bot = TeleBot(settings.tg_bot.telegram_token)


async def set_webhook():
    bot.remove_webhook()

    await asyncio.sleep(1)

    webhook_info = apihelper.get_webhook_info(settings.tg_bot.webhook_url)
    if webhook_info.get("url") != settings.tg_bot.webhook_url:
        bot.set_webhook(url=settings.tg_bot.webhook_url)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(message, "Привет! Я Telegram-бот с FastAPI!")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f"Вы написали: {message.text}")
