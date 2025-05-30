from dishka import Provider, Scope, provide

from config.app import AppSettings
from config.db import DBSettings
from config.telegram import TelegramSettings


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_tg_config(self) -> TelegramSettings:
        return TelegramSettings()

    @provide
    def get_db_config(self) -> DBSettings:
        return DBSettings()

    @provide
    def get_app_config(
        self, tg_config: TelegramSettings, db_config: DBSettings
    ) -> AppSettings:
        return AppSettings(tg_config=tg_config, db_config=db_config)
