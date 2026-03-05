import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import Config, load_config
import handlers
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import handlers


logger = logging.getLogger(__name__)



async def main():
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )

    logger.info("Starting bot")

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(router=handlers)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
    
