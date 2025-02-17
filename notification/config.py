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


class KafkaSettings(BaseSettings):
    """Настройки Kafka."""

    broker: str = "localhost:9092"

    class Config:
        env_prefix = "KAFKA__"


class NotificationSettings(BaseSettings):
    """Настройки сервиса уведомлений."""

    topic: str = "reminders"
    client_id: str = "reminder_consumer"

    class Config:
        env_prefix = "NOTIFICATION__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()
    api: ApiSettings = ApiSettings()
    kafka: KafkaSettings = KafkaSettings()
    notification: NotificationSettings = NotificationSettings()


settings = Settings()
