import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


class DbSettings(BaseSettings):
    """Настройки базы данных."""

    db_url: str = "postgresql+asyncpg://{user}:{password}@postgres:5432/{db}".format(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        db=POSTGRES_DB,
    )
    echo: bool = True


class TelegramBotSettings(BaseSettings):
    """Настройки телеграмм бота."""

    telegram_token: str = TELEGRAM_TOKEN
    webhook_url: str = WEBHOOK_URL


class Settings(BaseSettings):
    """Базовые настройки для приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()
    db: DbSettings = DbSettings()


settings = Settings()
