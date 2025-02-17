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


class Settings(BaseSettings):
    """Общие настройки приложения."""

    db: DbSettings = DbSettings()


settings = Settings()
