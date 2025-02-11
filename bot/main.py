import asyncio

import uvicorn
from config import settings
from fastapi import FastAPI, HTTPException, Request
from telebot import types

from bot import tg_bot

app = FastAPI()


async def set_webhook():
    tg_bot.delete_webhook(drop_pending_updates=True)

    await asyncio.sleep(1)

    tg_bot.set_webhook(url=settings.tg_bot.webhook_url)


@app.post("/")
async def telegram_webhook(request: Request):
    try:
        json_data = await request.json()
        update = types.Update.de_json(json_data)
        tg_bot.process_new_updates([update])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


if __name__ == "__main__":

    asyncio.run(set_webhook())
    uvicorn.run("main:app", reload=True, port=8001)
