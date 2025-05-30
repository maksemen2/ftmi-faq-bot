from pathlib import Path
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore",
    )

    user: Optional[str] = None
    password: Optional[SecretStr] = None
    host: Optional[str] = None
    port: Optional[int] = None
    name: str

    @property
    def dsn(self) -> str:
        """
        Создает строку подключения к базе данных через SQLAlchemy.
        """
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
