from dishka import Provider, Scope, provide

from domain.repository.question import QuestionRepository
from domain.services.question import QuestionService, QuestionServiceImpl


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_service(self, repo: QuestionRepository) -> QuestionService:
        return QuestionServiceImpl(repo)
