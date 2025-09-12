from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
import asyncio
from aiohttp import web, ClientSession
import os
import aiohttp

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
    return runner


async def aggressive_ping():
    await asyncio.sleep(30)

    while True:
        try:
            async with ClientSession() as session:
                url = f'https://{os.environ.get("RENDER_EXTERNAL_HOSTNAME", "ai-filmbot.onrender.com")}/healthz'
                async with session.get(url, timeout=15) as response:
                    if response.status == 200:
                        print("Self-ping executed successfully")
        except asyncio.TimeoutError:
            print("Ping timeout")
        except aiohttp.ClientConnectorError:
            print("Connection error")
        except Exception as e:
            print(f"Ping error: {e}")

        await asyncio.sleep(120)


async def run_bot():
    try:
        bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

        dp.include_router(start.router)
        dp.include_router(code_handler.router)

        await bot.delete_webhook(drop_pending_updates=True)
        print("Bot started successfully")
        await dp.start_polling(bot)

    except Exception as e:
        print(f"Bot error: {e}")
        await asyncio.sleep(30)
        await run_bot()


async def main():
    print("Starting application...")

    try:
        http_runner = await start_http_server()
        asyncio.create_task(aggressive_ping())
        await asyncio.sleep(5)
        await run_bot()

    except Exception as e:
        print(f"Critical error: {e}")
        await asyncio.sleep(60)
        asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())