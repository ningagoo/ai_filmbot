from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from bot.utils.subscription import check_subscription
from bot.utils.data_loader import get_movie_by_code
from bot.config import config
import os

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

@router.message(F.text)
async def handle_code(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(message.bot, user_id, config.CHANNEL_IDS)

    if not is_subscribed:
        return await message.answer(
            "❌ Для использования бота необходимо быть подписанным на каналы спонсоров:",
            reply_markup=get_subscribe_keyboard()
        )

    code = message.text.strip()
    movie = get_movie_by_code(code)

    if not movie:
        return await message.answer("😕 Неверный код. Попробуй другой.")

    text = f"<b>{movie['title']}</b>\n\n{movie.get('description', '')}"
    photo_path = movie.get("photo")

    if photo_path and os.path.exists(photo_path):

        photo_file = FSInputFile(photo_path)
        await message.answer_photo(photo=photo_file, caption=text, parse_mode=ParseMode.HTML)
    else:
        await message.answer(text, parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "check_subs")
async def check_subs_callback(callback: CallbackQuery):
    is_subscribed = await check_subscription(callback.bot, callback.from_user.id, config.CHANNEL_IDS)

    if not is_subscribed:
        await callback.answer("❌ Вы ещё не подписаны!", show_alert=True)
    else:
        await callback.message.edit_text("✅ Отлично! Теперь можешь отправить код и получить фильм/аниме/сериал.")
        await callback.answer()