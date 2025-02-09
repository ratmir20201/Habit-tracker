import asyncio

from telebot import TeleBot
from test_config import settings

tg_bot = TeleBot(settings.tg_bot.token)


async def set_webhook():
    tg_bot.delete_webhook(drop_pending_updates=True)

    await asyncio.sleep(1)

    tg_bot.set_webhook(url=settings.tg_bot.webhook_url)
    print(f"Webhook установлен на {settings.tg_bot.webhook_url}")


from handlers import *  # noqa

if __name__ == "__main__":
    tg_bot.infinity_polling()
