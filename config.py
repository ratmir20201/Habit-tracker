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
    echo: bool = True

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


class TelegramBotSettings(BaseSettings):
    """Настройки телеграмм бота."""

    token: str = ""
    webhook_url: str = ""

    class Config:
        env_prefix = "TG__"


class AccessTokenSettings(BaseSettings):
    """Настройки токена для аутентификации."""

    lifetime_seconds: int = 3600
    reset_password_token_secret: str = ""
    verification_token_secret: str = ""

    class Config:
        env_prefix = "ACCESS_TOKEN__"


class ApiSettings(BaseSettings):
    superuser_name: str = "admin"
    superuser_email: str = "admin@admin.com"
    superuser_password: str = "admin"

    class Config:
        env_prefix = "API__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()
    db: DbSettings = DbSettings()
    access_token: AccessTokenSettings = AccessTokenSettings()
    api: ApiSettings = ApiSettings()


settings = Settings()
