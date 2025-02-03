from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TelegramBotSettings(BaseSettings):
    """Настройки телеграмм бота."""

    token: str = ""
    webhook_url: str = ""

    class Config:
        env_prefix = "TG__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()


settings = Settings()
