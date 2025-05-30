from typing import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from delivery.telegram.keyboards.callback_data import (
    QUESTIONS_PER_PAGE,
    AddQuestionConfirmCallbackData,
    ConfirmAction,
    ListedQuestionAction,
    ListedQuestionCallbackData,
    QuestionEditAction,
    QuestionEditAgreeCallbackData,
    QuestionEditCallbackData,
    QuestionPaginatorCallbackData,
)
from domain.entities.question import QuestionListItem


def build_listed_questions_edit_kb(
    questions: Sequence[QuestionListItem], current_page: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for question in questions:
        builder.button(
            text=question.name,
            callback_data=ListedQuestionCallbackData(
                action=ListedQuestionAction.EDIT, question_id=question.id
            ),
        )
    if questions:
        builder.adjust(1)

    show_prev_button = current_page > 0
    show_next_button = len(questions) == QUESTIONS_PER_PAGE

    pagination_buttons_added_count = 0
    if show_prev_button:
        builder.button(
            text="⬅️", callback_data=QuestionPaginatorCallbackData(page=current_page - 1)
        )
        pagination_buttons_added_count += 1

    if show_next_button:
        builder.button(
            text="➡️", callback_data=QuestionPaginatorCallbackData(page=current_page + 1)
        )
        pagination_buttons_added_count += 1

    if pagination_buttons_added_count > 0:
        builder.adjust(pagination_buttons_added_count)

    builder.button(text="Добавить вопрос", callback_data="add_question")
    builder.adjust(1)

    return builder.as_markup()


def build_question_edit_kb(
    question_id: int, last_callback: str
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить название",
        callback_data=QuestionEditCallbackData(
            action=QuestionEditAction.NAME, question_id=question_id
        ),
    )
    builder.button(
        text="Изменить ответ",
        callback_data=QuestionEditCallbackData(
            action=QuestionEditAction.ANSWER, question_id=question_id
        ),
    )
    builder.button(
        text="Удалить вопрос",
        callback_data=QuestionEditCallbackData(
            action=QuestionEditAction.DELETE, question_id=question_id
        ),
    )

    builder.button(text="Назад", callback_data=last_callback)

    builder.adjust(1)

    return builder.as_markup()


def build_agree_kb(
    action: QuestionEditAction, question_id: int, last_callback_data: str
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да",
        callback_data=QuestionEditAgreeCallbackData(
            action=action, question_id=question_id
        ),
    )
    builder.button(text="Нет", callback_data=last_callback_data)
    return builder.as_markup()


def build_add_question_confirm_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(
        text="✅ Да",
        callback_data=AddQuestionConfirmCallbackData(action=ConfirmAction.YES),
    )
    b.button(
        text="❌ Нет",
        callback_data=AddQuestionConfirmCallbackData(action=ConfirmAction.NO),
    )
    return b.as_markup()
