from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


async def custom_unauthorized_handler(request: Request, exc):
    """Обработчик 401 кода ответа."""
    return JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"detail": "Ошибка авторизации. Пожалуйста, войдите в систему."},
    )


async def custom_forbid_handler(request: Request, exc):
    """Обработчик 403 кода ответа."""
    return JSONResponse(
        status_code=HTTP_403_FORBIDDEN,
        content={"detail": "У вас недостаточно прав для данной операции."},
    )
