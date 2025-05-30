import asyncio
import logging

from config.telegram import TelegramSettings
from delivery.telegram.factory import run_bot
from infrastructure.DI.factory import create_dishka

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def main():
    container = create_dishka()

    tg_settings = await container.get(TelegramSettings)
    await run_bot(
        container,
        mod_chat_id=tg_settings.mod_channel,
        bot_token=tg_settings.bot_token.get_secret_value(),
    )


if __name__ == "__main__":
    asyncio.run(main())
