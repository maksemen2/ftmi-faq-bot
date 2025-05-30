from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from delivery.telegram.keyboards.callback_data import (
    QUESTIONS_PER_PAGE,
    ListedQuestionCallbackData,
    QuestionEditAction,
)
from delivery.telegram.keyboards.moderator.questions_edit import (
    build_agree_kb,
    build_listed_questions_edit_kb,
    build_question_edit_kb,
)
from domain.entities.question import QuestionEntity
from domain.services.question import QuestionService


async def render_list(
    target: Message | CallbackQuery,
    service: QuestionService,
    page: int = 0,
) -> None:
    questions = await service.list_questions(page, QUESTIONS_PER_PAGE)
    kb = build_listed_questions_edit_kb(questions, current_page=page)
    text = "Выберите действие:"
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=kb)
    else:
        await target.answer(text, reply_markup=kb)


async def render_detail(
    target: Message | CallbackQuery,
    question: QuestionEntity,
    last_callback: str,
) -> None:
    text = f"{question.name}\n\n{question.answer}\n\nВыберите действие:"
    kb = build_question_edit_kb(question.id, last_callback)
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=kb)
    else:
        await target.answer(text, reply_markup=kb)


async def render_delete_confirm(
    target: Message | CallbackQuery,
    question_id: int,
    last: ListedQuestionCallbackData,
) -> None:
    kb = build_agree_kb(QuestionEditAction.DELETE, question_id, last)
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(
            "Вы уверены, что хотите удалить этот вопрос?",
            reply_markup=kb,
        )
    else:
        await target.answer(
            "Вы уверены, что хотите удалить этот вопрос?",
            reply_markup=kb,
        )
