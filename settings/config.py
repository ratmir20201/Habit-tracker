from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DbSettings(BaseSettings):
    """Настройки базы данных."""

    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "postgres"
    db_port: int = 5432
    db_name: str = ""
    echo: bool = True

    @property
    def db_url(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            name=self.db_name,
        )

    model_config = SettingsConfigDict(env_file=".env", env_prefix="POSTGRES_")


class TelegramBotSettings(BaseSettings):
    """Настройки телеграмм бота."""

    token: str = ""
    webhook_url: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="TELEGRAM_")


class Settings(BaseSettings):
    """Общие настройки приложения."""

    tg_bot: TelegramBotSettings = TelegramBotSettings()
    db: DbSettings = DbSettings()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
