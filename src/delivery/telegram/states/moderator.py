from aiogram.fsm.state import State, StatesGroup


class ModeratorSG(StatesGroup):
    waiting_new_question_value = State()


class AddQuestionSG(StatesGroup):
    waiting_question_name = State()
    waiting_question_answer = State()
    waiting_confirmation = State()


class UserQuestionAnswerSG(StatesGroup):
    waiting_question_answer = State()
