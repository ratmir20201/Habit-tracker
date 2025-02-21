import uvicorn
from fastapi import FastAPI, HTTPException, Request
from telebot import types, logger

from bot import tg_bot, set_webhook


async def lifespan(app: FastAPI):
    await set_webhook()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def telegram_webhook(request: Request):
    try:
        json_data = await request.json()
        logger.info("Получен Webhook: %s", json_data)
        update = types.Update.de_json(json_data)
        tg_bot.process_new_updates([update])
    except Exception as e:
        logger.info("Ошибка Webhook: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001, host="0.0.0.0")
