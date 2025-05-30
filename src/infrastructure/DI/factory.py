from dishka import AsyncContainer, make_async_container

from infrastructure.DI.config import ConfigProvider
from infrastructure.DI.db import DBProvider, RepositoryProvider
from infrastructure.DI.service import ServiceProvider


def create_dishka() -> AsyncContainer:
    return make_async_container(
        ConfigProvider(), DBProvider(), RepositoryProvider(), ServiceProvider()
    )
