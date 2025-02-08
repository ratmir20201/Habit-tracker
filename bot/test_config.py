from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TelegramBotSettings(BaseSettings):
    """Настройки телеграмм бота."""

    token: str = ""
    webhook_url: str = ""

    class Config:
        env_prefix = "TG__"


class ApiSettings(BaseSettings):
    url: str = "http://localhost:8000"

    class Config:
        env_prefix = "API__"


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    token_expire: int = 3600

    class Config:
        env_prefix = "REDIS__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()
    api: ApiSettings = ApiSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
