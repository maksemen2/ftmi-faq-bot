from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from domain.entities.question import QuestionEntity, QuestionListItem
from domain.exceptions.question import QuestionNotFoundError
from domain.repository.question import QuestionRepository
from infrastructure.database.models.question import QuestionModel


class SQLAlchemyQuestionRepository(QuestionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, question_id: int) -> QuestionEntity:
        stmt = select(QuestionModel).where(QuestionModel.id == question_id)
        result = await self._session.execute(stmt)
        try:
            question_model = result.scalars().first()
            return QuestionEntity.model_validate(question_model)
        except NoResultFound as exc:
            raise QuestionNotFoundError(question_id) from exc

    async def paginate(self, page: int, per_page: int) -> Sequence[QuestionListItem]:
        offset = page * per_page
        stmt = (
            select(QuestionModel)
            .options(load_only(QuestionModel.id, QuestionModel.name))
            .order_by(QuestionModel.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [QuestionListItem.model_validate(m) for m in models]

    async def add(self, name: str, answer: str) -> QuestionEntity:
        question_model = QuestionModel(name=name, answer=answer)
        self._session.add(question_model)

        await self._session.flush([question_model])
        await self._session.refresh(question_model)

        return QuestionEntity.model_validate(question_model)

    async def delete(self, question_id: int) -> None:
        stmt = delete(QuestionModel).where(QuestionModel.id == question_id)
        try:
            await self._session.execute(stmt)
        except NoResultFound as exc:
            raise QuestionNotFoundError(question_id) from exc

    async def update_name(self, question_id: int, name: str) -> QuestionEntity:
        stmt = (
            update(QuestionModel)
            .where(QuestionModel.id == question_id)
            .values(name=name)
            .returning(QuestionModel)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            raise QuestionNotFoundError(question_id)
        return QuestionEntity.model_validate(model)

    async def update_answer(self, question_id: int, answer: str) -> QuestionEntity:
        stmt = (
            update(QuestionModel)
            .where(QuestionModel.id == question_id)
            .values(answer=answer)
            .returning(QuestionModel)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            raise QuestionNotFoundError(question_id)
        return QuestionEntity.model_validate(model)

    async def commit(self) -> None:
        await self._session.commit()
