from aiogram.fsm.state import State, StatesGroup


class AskQuestionSG(StatesGroup):
    waiting_question = State()
