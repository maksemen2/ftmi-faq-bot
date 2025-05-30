from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from config.telegram import TelegramSettings
from delivery.telegram.keyboards.back import build_back_kb
from delivery.telegram.keyboards.callback_data import (
    QUESTIONS_PER_PAGE,
    ListedQuestionAction,
    ListedQuestionCallbackData,
    QuestionPaginatorCallbackData,
)
from delivery.telegram.keyboards.moderator.questions_answer import (
    build_question_answer_kb,
)
from delivery.telegram.keyboards.user.questions import build_listed_questions_view_kb
from delivery.telegram.states.user import AskQuestionSG
from delivery.telegram.utils.pagination_helpers import get_paginated_items
from domain.services.question import QuestionService

questions_router = r = Router(name="questions")

BASE_TEXT_LIST_QUESTIONS = "Список вопросов:\n\nЕсли вы не нашли тут интересующий вас вопрос, вы можете обратиться к организатором по почте osk_ftmi@edu.itmo.ru или задать вопрос модераторам, используя кнопку 'задать свой вопрос'"


@r.callback_query(F.data == "list_questions")
@inject
async def on_list_questions(call: CallbackQuery, service: FromDishka[QuestionService]):
    questions = await service.list_questions(0, QUESTIONS_PER_PAGE)

    if not questions:
        await call.message.answer(
            "Пока нет доступных вопросов. Вы можете задать свой вопрос.",
            reply_markup=build_listed_questions_view_kb([], 0),
        )
        return

    await call.message.answer(
        BASE_TEXT_LIST_QUESTIONS,
        reply_markup=build_listed_questions_view_kb(questions, 0),
    )


@r.callback_query(
    ListedQuestionCallbackData.filter(F.action == ListedQuestionAction.SHOW)
)
@inject
async def on_show_question(
    call: CallbackQuery,
    callback_data: ListedQuestionCallbackData,
    service: FromDishka[QuestionService],
):
    question_id = callback_data.question_id
    question = await service.get_question(question_id)

    if question is None:
        await call.answer("Вопрос не найден.", show_alert=True)
        return

    text = f"<b>{question.name}</b>\n\n{question.answer}"

    await call.message.edit_text(text, reply_markup=build_back_kb("list_questions"))


@r.callback_query(QuestionPaginatorCallbackData.filter())
@inject
async def on_page_change(
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
        await call.message.edit_text(
            BASE_TEXT_LIST_QUESTIONS,
            reply_markup=build_listed_questions_view_kb(questions, page),
        )


@r.callback_query(F.data == "stop_ask_question")
async def on_stop_ask_question(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()


@r.callback_query(F.data == "ask")
async def on_ask_question(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Пожалуйста, напишите ваш вопрос. Модераторы ответят на него в ближайшее время.",
        reply_markup=build_back_kb("stop_ask_question"),
    )
    await state.set_state(AskQuestionSG.waiting_question)
    await call.answer()


@r.message(AskQuestionSG.waiting_question)
@inject
async def on_question_received(
    message: Message,
    bot: Bot,
    state: FSMContext,
    settings: FromDishka[TelegramSettings],
):
    question_text = message.html_text

    mod_channel_id = settings.mod_channel

    await bot.send_message(
        mod_channel_id,
        f"Пользователь {message.from_user.mention_html()} задал вопрос:\n\n{question_text}",
        reply_markup=build_question_answer_kb(message.from_user.id, message.message_id),
    )
    await message.answer(
        "Ваш вопрос получен! Модератор ответит на него в ближайшее время."
    )
    await state.clear()
