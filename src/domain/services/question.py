from abc import ABC, abstractmethod
from typing import Sequence

from domain.exceptions.question import QuestionNotFoundError
from domain.repository.question import QuestionRepository
from domain.entities.question import QuestionEntity, QuestionListItem

class QuestionService(ABC):
    
    @abstractmethod
    async def list_questions(self, page: int, per_page: int) -> Sequence[QuestionListItem]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_question(self, question_id: int) -> QuestionEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def add_question(self, name: str, answer: str) -> QuestionEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def update_question_name(self, question_id: int, name: str) -> QuestionEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def update_question_answer(self, question_id: int, answer: str) -> QuestionEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_question(self, question_id: int) -> None:
        raise NotImplementedError

class QuestionServiceImpl(QuestionService):
    def __init__(self, repository: QuestionRepository):
        self.repo = repository
        
    async def list_questions(self, page: int, per_page: int) -> Sequence[QuestionListItem]:
        return await self.repo.paginate(page, per_page)
    
    async def get_question(self, question_id: int) -> QuestionEntity:
        return await self.repo.get_by_id(question_id)
    
    async def add_question(self, name: str, answer: str) -> QuestionEntity:
        entity = await self.repo.add(name, answer)
        await self.repo.commit()
        return entity

    async def update_question_name(self, question_id: int, name: str) -> QuestionEntity:
        entity = await self.repo.update_name(question_id, name)
        await self.repo.commit()
        return entity
    
    async def update_question_answer(self, question_id: int, answer: str) -> QuestionEntity:
        entity = await self.repo.update_answer(question_id, answer)
        await self.repo.commit()
        return entity
    
    async def delete_question(self, question_id: int) -> None:
        await self.repo.delete(question_id)
        await self.repo.commit()