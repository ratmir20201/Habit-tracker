import asyncio

import uvicorn
from fastapi import HTTPException, Request
from telebot import types

from api.main import get_app
from bot.main import tg_bot, set_webhook

app = get_app()


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
    # Бот не показывает команды в папке handlers нужно исправить
    uvicorn.run("main:app", reload=True)
