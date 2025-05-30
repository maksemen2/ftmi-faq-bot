from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message


class ModChatFilter(Filter):
    def __init__(self, mod_chat_id: int):
        self.mod_chat_id = mod_chat_id

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        if isinstance(update, Message):
            print(self.mod_chat_id)
            return update.chat.id == self.mod_chat_id
        elif isinstance(update, CallbackQuery):
            print(self.mod_chat_id)
            return update.message.chat.id == self.mod_chat_id
        return False
