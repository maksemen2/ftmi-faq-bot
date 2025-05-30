from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from delivery.telegram.keyboards.user.start import build_start_kb

start_router = r = Router(name="start")


@r.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я - бот, который поможет тебе ответить на вопрос, связанный с конференцией ФТМИ. Используй клавиатуру ниже:",
        reply_markup=build_start_kb(),
    )
