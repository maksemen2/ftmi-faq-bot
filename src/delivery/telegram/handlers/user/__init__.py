from aiogram import Router

from delivery.telegram.handlers.user.questions import questions_router
from delivery.telegram.handlers.user.start import start_router

user_router = Router(name="user")

user_router.include_routers(questions_router, start_router)

__all__ = [
    "user_router",
]
