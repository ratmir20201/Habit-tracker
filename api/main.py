import uvicorn
from fastapi import FastAPI

from api.actions.create_superuser import create_superuser
from api.authentication.auth_router import router as auth_roter
from api.routes.router import main_router
from config import settings


async def lifespan(app: FastAPI):
    await create_superuser(
        email=settings.api.superuser_email,
        username=settings.api.superuser_name,
        password=settings.api.superuser_password,
    )
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)
app.include_router(auth_roter)


def get_app() -> FastAPI:
    return app


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
