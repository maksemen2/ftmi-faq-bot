from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from delivery.telegram.handlers.moderator.questions_render import (
    render_delete_confirm,
    render_detail,
    render_list,
)
from delivery.telegram.keyboards.back import build_back_kb
from delivery.telegram.keyboards.callback_data import (
    QUESTIONS_PER_PAGE,
    ListedQuestionAction,
    ListedQuestionCallbackData,
    QuestionEditAction,
    QuestionEditAgreeCallbackData,
    QuestionEditCallbackData,
    QuestionPaginatorCallbackData,
)
from delivery.telegram.states.moderator import ModeratorSG
from delivery.telegram.utils.pagination_helpers import get_paginated_items
from domain.services.question import QuestionService

questions_edit_router = r = Router(name="questions_edit")


@r.message(Command("edit"))
@inject
async def cmd_edit(message: Message, service: FromDishka[QuestionService]):
    await render_list(message, service, page=0)


@r.callback_query(F.data == "render_list")
@inject
async def on_render_list(call: CallbackQuery, service: FromDishka[QuestionService]):
    await render_list(call, service, page=0)


@r.callback_query(QuestionPaginatorCallbackData.filter())
@inject
async def on_page(
    call: CallbackQuery,
    callback_data: QuestionPaginatorCallbackData,
    service: FromDishka[QuestionService],
):
    page = callback_data.page
    questions = await get_paginated_items(
        call=call,
        list_method=service.list_questions,
        page=page,
        per_page=QUESTIONS_PER_PAGE,
    )
    if questions is not None:
        await render_list(call, service, page=page)


@r.callback_query(
    ListedQuestionCallbackData.filter(F.action == ListedQuestionAction.EDIT)
)
@inject
async def on_show(
    call: CallbackQuery,
    callback_data: ListedQuestionCallbackData,
    service: FromDishka[QuestionService],
):
    question = await service.get_question(callback_data.question_id)
    await render_detail(call, question, "render_list")


@r.callback_query(F.data == "stop_edit")
@inject
async def on_stop_edit(
    call: CallbackQuery, state: FSMContext, service: FromDishka[QuestionService]
):
    question = await service.get_question(await state.get_value("question_id"))
    await state.clear()
    await render_detail(call, question, "render_list")


@r.callback_query(
    QuestionEditCallbackData.filter(F.action != QuestionEditAction.DELETE)
)
async def on_start_edit(
    call: CallbackQuery,
    callback_data: QuestionEditCallbackData,
    state: FSMContext,
):
    await state.set_state(ModeratorSG.waiting_new_question_value)
    await state.update_data(
        question_id=callback_data.question_id,
        action=callback_data.action,
        to_delete=call.message.message_id,
    )
    await call.message.edit_text(
        "Введите новое значение:", reply_markup=build_back_kb("stop_edit")
    )


@r.message(ModeratorSG.waiting_new_question_value)
@inject
async def on_new_value(
    message: Message, bot: Bot, state: FSMContext, service: FromDishka[QuestionService]
):
    data = await state.get_data()
    qid, action, msg_id = data["question_id"], data["action"], data["to_delete"]
    if action == QuestionEditAction.NAME:
        await service.update_question_name(qid, message.text)
    else:
        await service.update_question_answer(qid, message.html_text)
    await bot.delete_message(message.chat.id, msg_id)
    await message.answer("Вопрос успешно изменён.")
    question = await service.get_question(qid)
    await render_detail(message, question, "render_list")
    await state.clear()


@r.callback_query(
    QuestionEditCallbackData.filter(F.action == QuestionEditAction.DELETE)
)
async def on_delete(
    call: CallbackQuery,
    callback_data: QuestionEditCallbackData,
):
    back_to_detail_callback = ListedQuestionCallbackData(
        action=ListedQuestionAction.EDIT, question_id=callback_data.question_id
    ).pack()

    await render_delete_confirm(
        call, callback_data.question_id, back_to_detail_callback
    )


@r.callback_query(
    QuestionEditAgreeCallbackData.filter(F.action == QuestionEditAction.DELETE)
)
@inject
async def on_delete_confirm(
    call: CallbackQuery,
    callback_data: QuestionEditAgreeCallbackData,
    service: FromDishka[QuestionService],
):
    await service.delete_question(callback_data.question_id)
    await call.answer("Вопрос удалён.")
    await render_list(call, service, page=0)
