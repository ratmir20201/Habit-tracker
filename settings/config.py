import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

TOKEN = os.getenv("TOKEN")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


class Settings(BaseSettings):
    """Базовые настройки для приложения."""

    token: str = TOKEN
    db_url: str = "postgresql+asyncpg://{user}:{password}@postgres:5432/{db}".format(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        db=POSTGRES_DB,
    )
    echo: bool = True


settings = Settings()
