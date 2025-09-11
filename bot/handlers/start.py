from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.utils.subscription import check_subscription
from bot.config import config

router = Router()

def get_subscribe_keyboard():
    if not config.CHANNEL_LINKS:
        return None
    keyboard = [
        [InlineKeyboardButton(text="📢 Подписаться", url=link)]
        for link in config.CHANNEL_LINKS
    ]
    keyboard.append([InlineKeyboardButton(text="✅ Я подписался", callback_data="check_subs")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    is_subscribed = await check_subscription(message.bot, message.from_user.id, config.CHANNEL_IDS)

    if not is_subscribed:
        return await message.answer(
            "❌ Пожалуйста, подпишитесь на каналы спонсоров, чтобы пользоваться ботом:",
            reply_markup=get_subscribe_keyboard()
        )

    await message.answer("👋 Привет! Отправь код, чтобы получить фильм/аниме/сериал.")

@router.callback_query(F.data == "check_subs")
async def check_subs_callback(callback: CallbackQuery):
    is_subscribed = await check_subscription(callback.bot, callback.from_user.id, config.CHANNEL_IDS)

    if not is_subscribed:
        await callback.answer("❌ Вы ещё не подписаны!", show_alert=True)
    else:
        await callback.message.edit_text("✅ Спасибо за подписку! Теперь отправь код, чтобы получить фильм/аниме/сериал.")
        await callback.answer()