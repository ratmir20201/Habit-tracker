import uvicorn
from actions.create_superuser import create_superuser
from authentication.auth_router import router as auth_roter
from cache import init_cache
from config import settings
from exceptions.handlers import (custom_forbid_handler,
                                 custom_unauthorized_handler)
from fastapi import FastAPI
from middlewares.exception import ExceptionHandleMiddleware
from middlewares.logging import LoggingMiddleware
from routes.router import main_router
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


async def lifespan(app: FastAPI):
    """Перед запуском приложения создает superuser'а и инициализирует кэш."""

    await create_superuser(
        email=settings.api.superuser_email,
        username=settings.api.superuser_name,
        password=settings.api.superuser_password,
    )
    await init_cache()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)
app.include_router(auth_roter)

app.add_exception_handler(HTTP_401_UNAUTHORIZED, custom_unauthorized_handler)
app.add_exception_handler(HTTP_403_FORBIDDEN, custom_forbid_handler)

app.add_middleware(LoggingMiddleware)
app.add_middleware(ExceptionHandleMiddleware)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
