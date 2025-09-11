from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
import asyncio
from aiohttp import web
import os

from bot.handlers import start, code_handler
from bot.config import config



async def health_check(request):
    return web.Response(text="OK", status=200)


async def start_http_server():
    app = web.Application()
    app.router.add_get('/healthz', health_check)
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get('PORT', 8000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"HTTP server started on port {port}")


async def main():

    asyncio.create_task(start_http_server())

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