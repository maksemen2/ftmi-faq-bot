from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from delivery.telegram.handlers.moderator.question_add_utils import show_preview
from delivery.telegram.handlers.moderator.questions_render import render_list
from delivery.telegram.keyboards.back import build_back_kb
from delivery.telegram.keyboards.callback_data import (
    AddQuestionConfirmCallbackData,
    ConfirmAction,
)
from delivery.telegram.keyboards.moderator.questions_edit import (
    build_add_question_confirm_kb,
)
from delivery.telegram.states.moderator import AddQuestionSG
from domain.services.question import QuestionService

question_add_router = r = Router(name="question_add")


async def prompt_question_name(
    target: Message | CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(AddQuestionSG.waiting_question_name)
    kb = build_back_kb("stop_add_question")
    if isinstance(target, CallbackQuery):
        await target.message.edit_text("Введите название вопроса:", reply_markup=kb)
    else:
        await target.answer("Введите название вопроса:", reply_markup=kb)


async def prompt_question_answer(message: Message, state: FSMContext) -> None:
    await state.update_data(question_name=message.text)
    await state.set_state(AddQuestionSG.waiting_question_answer)
    kb = build_back_kb("back_to_name")
    await message.answer("Введите ответ на вопрос:", reply_markup=kb)


@r.callback_query(F.data.in_(["add_question", "back_to_name"]))
async def start_add_flow(call: CallbackQuery, state: FSMContext) -> None:
    await prompt_question_name(call, state)


@r.callback_query(F.data == "stop_add_question")
@inject
async def stop_add_flow(
    call: CallbackQuery, state: FSMContext, service: FromDishka[QuestionService]
) -> None:
    await state.clear()
    await render_list(call, service)


@r.message(AddQuestionSG.waiting_question_name)
async def receive_question_name(message: Message, state: FSMContext) -> None:
    await prompt_question_answer(message, state)


@r.message(AddQuestionSG.waiting_question_answer)
async def receive_question_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    name = data.get("question_name")
    answer = message.text or ""
    if not name or not answer.strip():
        await message.answer(
            "Название и ответ не могут быть пустыми. Пожалуйста, попробуйте снова."
        )
        return

    await state.update_data(question_answer=answer)
    await state.set_state(AddQuestionSG.waiting_confirmation)
    await show_preview(message, name, answer)


@r.callback_query(AddQuestionConfirmCallbackData.filter(F.action == ConfirmAction.YES))
@inject
async def confirm_add(
    call: CallbackQuery, state: FSMContext, service: FromDishka[QuestionService]
) -> None:
    data = await state.get_data()
    await service.add_question(data["question_name"], data["question_answer"])
    await state.clear()
    await call.message.answer("✅ Вопрос успешно добавлен!")
    await render_list(call, service)


@r.callback_query(AddQuestionConfirmCallbackData.filter(F.action == ConfirmAction.NO))
async def cancel_add(call: CallbackQuery, state: FSMContext) -> None:
    await prompt_question_name(call, state)
