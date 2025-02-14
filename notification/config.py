from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TelegramBotSettings(BaseSettings):
    """Настройки телеграмм бота."""

    token: str = ""

    class Config:
        env_prefix = "TG__"


class ApiSettings(BaseSettings):
    """Настройки api сервера."""

    url: str = "http://localhost:8000"
    superuser_email: str = "admin@admin.com"
    superuser_password: str = "admin"

    class Config:
        env_prefix = "API__"


class NotificationSettings(BaseSettings):
    """Настройки сервиса уведомлений."""

    hour_we_remind: int = 17
    timezone: str = "Asia/Almaty"

    class Config:
        env_prefix = "NOTIFICATION__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()
    api: ApiSettings = ApiSettings()
    notification: NotificationSettings = NotificationSettings()


settings = Settings()
