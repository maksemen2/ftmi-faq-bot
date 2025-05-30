from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message


class PrivateChatFilter(Filter):

    def _is_private_message(self, update: Message) -> bool:
        return update.chat.type == "private"

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        if isinstance(update, Message):
            return self._is_private_message(update)
        elif isinstance(update, CallbackQuery):
            return self._is_private_message(update.message)
        return False
