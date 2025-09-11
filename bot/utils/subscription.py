from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

async def check_subscription(bot: Bot, user_id: int, channel_ids: list[int]) -> bool:
    if not channel_ids:
        return True

    for channel_id in channel_ids:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status in ("left", "kicked"):
                return False
        except TelegramBadRequest:
            return False
    return True