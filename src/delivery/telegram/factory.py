from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from delivery.telegram.filters.private_message import PrivateChatFilter
from delivery.telegram.handlers.moderator import moderator_router
from delivery.telegram.handlers.user import user_router
from delivery.telegram.filters.mod_chat import ModChatFilter

from aiogram.fsm.strategy import FSMStrategy

def setup_routers(dp: Dispatcher, mod_chat_id: int) -> None:
    print(mod_chat_id)
    moderator_router.callback_query.filter(ModChatFilter(mod_chat_id=mod_chat_id))
    moderator_router.message.filter(ModChatFilter(mod_chat_id=mod_chat_id))
    
    user_router.message.filter(PrivateChatFilter())
    user_router.callback_query.filter(PrivateChatFilter())
    
    dp.include_routers(user_router, moderator_router)

async def run_bot(dishka: AsyncContainer, mod_chat_id: int, bot_token: str) -> None:
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))
    
    dp = Dispatcher(storage=MemoryStorage())
    
    setup_routers(dp, mod_chat_id)
    
    setup_dishka(dishka, dp)
    
    await dp.start_polling(bot)