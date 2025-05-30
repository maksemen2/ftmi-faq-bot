from abc import ABC, abstractmethod
from typing import Sequence

from domain.entities.question import QuestionListItem, QuestionEntity

class QuestionRepository(ABC):
    
    @abstractmethod
    async def get_by_id(self, question_id: int) -> QuestionEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def paginate(self, page: int, per_page: int) -> Sequence[QuestionListItem]:
        raise NotImplementedError
    
    @abstractmethod
    async def add(self, name: str, answer: str) -> QuestionEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, question_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_name(self, question_id: int, name: str) -> QuestionEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def update_answer(self, question_id: int, answer: str) -> QuestionEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError