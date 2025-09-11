from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
import asyncio
from dotenv import load_dotenv

from bot.handlers import start, code_handler
from bot.config import config

load_dotenv()

async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

    dp.include_router(start.router)
    dp.include_router(code_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())