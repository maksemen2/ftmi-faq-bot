from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from delivery.telegram.keyboards.callback_data import (
    ConfirmAction,
    UserQuestionCallbackData,
)


def build_question_answer_kb(
    from_user_id: int, question_message_id: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Ответить на вопрос",
        callback_data=UserQuestionCallbackData(
            action=ConfirmAction.YES,
            user_id=from_user_id,
            question_message_id=question_message_id,
        ),
    )

    builder.button(
        text="Отклонить вопрос",
        callback_data=UserQuestionCallbackData(
            action=ConfirmAction.NO,
            user_id=from_user_id,
            question_message_id=question_message_id,
        ),
    )

    return builder.as_markup()
