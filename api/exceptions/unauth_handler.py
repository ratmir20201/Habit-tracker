from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from api.main import app


@app.exception_handler(HTTP_401_UNAUTHORIZED)
async def custom_unauthorized_handler(request: Request, exc):
    return JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"detail": "Ошибка авторизации. Пожалуйста, войдите в систему."},
    )
