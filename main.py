from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
import asyncio
from aiohttp import web, ClientSession
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

    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"HTTP server started on port {port}")


async def aggressive_ping():
    """Агрессивный самопинг каждые 2 минуты"""
    while True:
        try:
            async with ClientSession() as session:
                async with session.get(
                        f'https://{os.environ.get("RENDER_EXTERNAL_HOSTNAME", "ai-filmbot.onrender.com")}/healthz',
                        timeout=10):
                    print("✅ Self-ping executed")
        except Exception as e:
            print(f"❌ Ping error: {e}")
        await asyncio.sleep(120)  # 2 минуты


async def main():
    try:
        asyncio.create_task(start_http_server())

        asyncio.create_task(aggressive_ping())

        bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

        dp.include_router(start.router)
        dp.include_router(code_handler.router)


        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Bot started successfully")
        await dp.start_polling(bot)

    except Exception as e:
        print(f"❌ Critical error in main: {e}")


if __name__ == "__main__":
    asyncio.run(main())