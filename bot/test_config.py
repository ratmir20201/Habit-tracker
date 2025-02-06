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

    # class Config:
    #     env_prefix = "API__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()
    api: ApiSettings = ApiSettings()


settings = Settings()
