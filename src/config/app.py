from pydantic_settings import BaseSettings

from config.db import DBSettings
from config.telegram import TelegramSettings

class AppSettings(BaseSettings):
    telegram: TelegramSettings
    database: DBSettings