from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TelegramBotSettings(BaseSettings):
    """Настройки телеграмм бота."""

    token: str = ""
    webhook_url: str = ""
    carry_over_complete_habits_days: int = 21
    debug_port: int = 8001

    class Config:
        env_prefix = "TG__"


class ApiSettings(BaseSettings):
    """Настройки api сервера."""

    url: str = "http://localhost:8000"

    class Config:
        env_prefix = "API__"


class RedisSettings(BaseSettings):
    """Настройки Redis."""

    host: str = "redis"
    port: int = 6379
    db: int = 0
    # Кол-во секунд которое хранится токен должен быть равным
    # access_token_settings.lifetime_seconds из каталога api
    token_expire: int = 3600

    class Config:
        env_prefix = "REDIS__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()
    api: ApiSettings = ApiSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
