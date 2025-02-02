import asyncio

from telebot import TeleBot

from config import settings

tg_bot = TeleBot(settings.tg_bot.token)


async def set_webhook():
    tg_bot.remove_webhook()
    # bot.delete_webhook(drop_pending_updates=True)

    await asyncio.sleep(1)

    tg_bot.set_webhook(url=settings.tg_bot.webhook_url)
    print(f"Webhook установлен на {settings.tg_bot.webhook_url}")


@tg_bot.message_handler(func=lambda message: True)
def echo_message(message):
    tg_bot.reply_to(message, "К сожалению я не знаю такой команды.")
