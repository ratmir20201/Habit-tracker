from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from telebot import types

from bot.bot import bot, set_webhook


@asynccontextmanager
async def lifespan(app: FastAPI):
    await set_webhook()
    print("WEBHOOK успешно подключился.")

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def telegram_webhook(request: Request):
    try:
        json_data = await request.json()
        update = types.Update.de_json(json_data)
        bot.process_new_updates([update])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
