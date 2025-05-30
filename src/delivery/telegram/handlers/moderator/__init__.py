from aiogram import Router

from delivery.telegram.handlers.moderator.question_add import question_add_router
from delivery.telegram.handlers.moderator.question_answer import question_answer_router
from delivery.telegram.handlers.moderator.questions_edit import questions_edit_router


moderator_router = Router(name="moderator")

moderator_router.include_routers(question_answer_router, question_add_router, questions_edit_router)

__all__ = [
    "moderator_router",
]