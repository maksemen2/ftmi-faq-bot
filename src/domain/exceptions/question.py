class DomainError(Exception):
    pass


class QuestionNotFoundError(DomainError):
    def __init__(self, question_id: str):
        super().__init__(f"Question with ID {question_id} not found.")
        self.question_id = question_id