import uvicorn
from actions.create_superuser import create_superuser
from authentication.auth_router import router as auth_roter
from cache import init_cache
from config import settings
from exceptions.unauth_handler import custom_unauthorized_handler
from fastapi import FastAPI
from routes.router import main_router
from starlette.status import HTTP_401_UNAUTHORIZED


async def lifespan(app: FastAPI):
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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
