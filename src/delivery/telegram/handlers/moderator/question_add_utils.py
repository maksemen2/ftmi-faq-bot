from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from delivery.telegram.keyboards.moderator.questions_edit import (
    build_add_question_confirm_kb,
)
from delivery.telegram.keyboards.back import build_back_kb
from delivery.telegram.states.moderator import AddQuestionSG


async def prompt_question_name(
    target: Message | CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(AddQuestionSG.waiting_question_name)
    kb = build_back_kb("stop_add_question")
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(
            "Введите название вопроса:", reply_markup=kb
        )
    else:
        await target.answer(
            "Введите название вопроса:", reply_markup=kb
        )


async def prompt_question_answer(
    message: Message, state: FSMContext
) -> None:
    await state.update_data(question_name=message.text)
    await state.set_state(AddQuestionSG.waiting_question_answer)
    kb = build_back_kb("back_to_name")
    await message.answer(
        "Введите ответ на вопрос:", reply_markup=kb
    )


async def show_preview(
    message: Message, question_name: str, question_answer: str
) -> None:
    preview = f"🔎 Предпросмотр 🔎\n\n<b>{question_name}</b>\n{question_answer}"
    await message.answer(
        preview, reply_markup=build_add_question_confirm_kb()
    )
    
