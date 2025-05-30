from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from delivery.telegram.keyboards.back import build_back_kb
from delivery.telegram.keyboards.callback_data import ConfirmAction, UserQuestionCallbackData
from delivery.telegram.states.moderator import UserQuestionAnswerSG

question_answer_router = r = Router(name="question_answer")

@r.callback_query(UserQuestionCallbackData.filter(F.action == ConfirmAction.NO))
async def on_user_question_decline(call: CallbackQuery):
    await call.message.edit_text(
        text=f"Отклонено модератором {call.from_user.mention_html()}\n\n<span class='tg-spoiler'>{call.message.text}</span>",
        reply_markup=call.message.reply_markup
    )

@r.callback_query(F.data == "stop_question_answer")
async def on_user_question_stop(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()

@r.callback_query(UserQuestionCallbackData.filter(F.action == ConfirmAction.YES))
async def on_user_question_accept(call: CallbackQuery, callback_data: UserQuestionCallbackData, state: FSMContext):
    print("setting state", UserQuestionAnswerSG.waiting_question_answer)
    await state.set_state(UserQuestionAnswerSG.waiting_question_answer)
    await state.update_data(
        from_user=callback_data.user_id,
        message_id=callback_data.question_message_id,
        to_edit=call.message.message_id,
        question_text=call.message.text
    )
    await call.message.reply(
        "Введите ответ на вопрос пользователя:",
        reply_markup=build_back_kb("stop_question_answer")
    )
    await call.message.edit_text(
        text=f"Отвечает модератор {call.from_user.mention_html()}\n\n<span class='tg-spoiler'>{call.message.text}</span>",
        reply_markup=call.message.reply_markup
    )

@r.message(StateFilter(UserQuestionAnswerSG.waiting_question_answer))
async def on_user_question_answer(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.send_message(
        data["from_user"],
        f"Модератор ответил на ваш вопрос:\n\n{message.html_text}",
        reply_to_message_id=data["message_id"]
    )
    await bot.edit_message_text(
        text=f"Отвечено модератором {message.from_user.mention_html()}\n\n<span class='tg-spoiler'>{data['question_text']}</span>",
        chat_id=message.chat.id,
        message_id=data["to_edit"],
    )
    
    await message.answer("Ответ успешно доставлен пользователю.")
    
    await state.clear()