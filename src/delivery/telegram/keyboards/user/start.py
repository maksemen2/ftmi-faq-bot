from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def build_start_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="FAQ",
        callback_data="list_questions"
    )
    
    return builder.as_markup()