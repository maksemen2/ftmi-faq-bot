from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path


class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TELEGRAM_", env_file=Path(__file__).resolve().parent.parent.parent / ".env", extra="ignore")

    bot_token: SecretStr
    mod_channel: int
