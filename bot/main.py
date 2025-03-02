import uvicorn
from config import settings
from fastapi import FastAPI, HTTPException, Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from telebot import logger, types

from bot import set_webhook, tg_bot


async def lifespan(app: FastAPI):
    """Перед запуском приложения устанавливает вебхук."""
    await set_webhook()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def telegram_webhook(request: Request):
    """Роут для получения данных через вебхук."""
    try:
        json_data = await request.json()
        logger.info("Получен Webhook: %s", json_data)
        update = types.Update.de_json(json_data)
        tg_bot.process_new_updates([update])
    except Exception as exc:
        logger.info("Ошибка Webhook: %s", str(exc))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=settings.tg_bot.debug_port)
