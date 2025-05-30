from typing import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from delivery.telegram.keyboards.callback_data import (
    QUESTIONS_PER_PAGE,
    ListedQuestionAction,
    ListedQuestionCallbackData,
    QuestionPaginatorCallbackData,
)
from domain.entities.question import QuestionListItem


def build_listed_questions_view_kb(
    questions: Sequence[QuestionListItem], current_page: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for question in questions:
        builder.button(
            text=question.name,
            callback_data=ListedQuestionCallbackData(
                action=ListedQuestionAction.SHOW, question_id=question.id
            ),
        )
    if questions:
        builder.adjust(1)

    show_prev_button = current_page > 0
    show_next_button = len(questions) > QUESTIONS_PER_PAGE

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

    builder.button(text="Задать свой вопрос", callback_data="ask")
    builder.adjust(1)

    return builder.as_markup()
