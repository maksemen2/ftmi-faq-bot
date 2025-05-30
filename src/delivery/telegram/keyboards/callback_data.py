from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

QUESTIONS_PER_PAGE = 5


class ListedQuestionAction(StrEnum):
    SHOW = "show"
    EDIT = "edit"


class ListedQuestionCallbackData(CallbackData, prefix="question"):
    action: ListedQuestionAction
    question_id: int


class QuestionEditAction(StrEnum):
    NAME = "name"
    ANSWER = "answer"
    DELETE = "delete"


class QuestionEditCallbackData(CallbackData, prefix="question_edit"):
    action: QuestionEditAction
    question_id: int


class QuestionPaginatorCallbackData(CallbackData, prefix="question_paginator"):
    page: int


class QuestionEditAgreeCallbackData(
    QuestionEditCallbackData, prefix="question_edit_agree"
): ...


class ConfirmAction(StrEnum):
    YES = "yes"
    NO = "no"


class AddQuestionConfirmCallbackData(CallbackData, prefix="add_q_confirm"):
    action: ConfirmAction


class UserQuestionCallbackData(CallbackData, prefix="user_question"):
    action: ConfirmAction
    user_id: int
    question_message_id: int
