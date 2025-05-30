from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config.db import DBSettings
from domain.repository.question import QuestionRepository
from infrastructure.database.repository.question import SQLAlchemyQuestionRepository


class DBProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, config: DBSettings) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(config.dsn)
        yield engine
        await engine.dispose()

    @provide
    async def get_connection(
        self, engine: AsyncEngine
    ) -> AsyncIterable[AsyncConnection]:
        async with engine.connect() as connection:
            yield connection

    @provide
    def get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_questions_repository(self, session: AsyncSession) -> QuestionRepository:
        repo = SQLAlchemyQuestionRepository(session)
        return repo
