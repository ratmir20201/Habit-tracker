from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DbSettings(BaseSettings):
    """Настройки базы данных."""

    user: str = "user"
    password: str = "password"
    host: str = "postgres"
    port: int = 5432
    name: str = ""
    echo: bool = False

    @property
    def db_url(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            name=self.name,
        )

    class Config:
        env_prefix = "DB__"


class AccessTokenSettings(BaseSettings):
    """Настройки токена для аутентификации."""

    lifetime_seconds: int = 3600
    reset_password_token_secret: str = ""
    verification_token_secret: str = ""

    class Config:
        env_prefix = "ACCESS_TOKEN__"


class ApiSettings(BaseSettings):
    """Настройки api сервера."""

    superuser_name: str = "admin"
    superuser_email: str = "admin@admin.com"
    superuser_password: str = "admin"

    cache_time: int = 60

    class Config:
        env_prefix = "API__"


class RedisSettings(BaseSettings):
    """Настройки Redis."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0

    @property
    def redis_url(self) -> str:
        return "redis://{host}:{port}/db".format(
            host=self.host,
            port=self.port,
            db=self.db,
        )

    class Config:
        env_prefix = "REDIS__"


class KafkaSettings(BaseSettings):
    """Настройки Kafka."""

    broker: str = "localhost:9092"

    class Config:
        env_prefix = "KAFKA__"


class NotificationSettings(BaseSettings):
    """Настройки сервиса уведомлений."""

    topic: str = "reminders"
    client_id: str = "reminder_producer"
    hour_we_remind: int = 18

    class Config:
        env_prefix = "NOTIFICATION__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    db: DbSettings = DbSettings()
    access_token: AccessTokenSettings = AccessTokenSettings()
    api: ApiSettings = ApiSettings()
    redis: RedisSettings = RedisSettings()
    kafka: KafkaSettings = KafkaSettings()
    notification: NotificationSettings = NotificationSettings()


settings = Settings()
