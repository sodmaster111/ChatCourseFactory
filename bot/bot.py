import asyncio
import os

import httpx

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import TELEGRAM_BOT_TOKEN, BACKEND_BASE_URL

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()


# КНОПКА "🎓 Начать обучение"
start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Начать обучение", callback_data="start_learning")]
    ]
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Приветствие: ТОЛЬКО ФОТО + кнопка «🎓 Начать обучение».
    Временно используем заглушку-картинку по URL.
    Позже можно заменить на свою картинку (file_id или URL).
    """

    photo_url = "https://picsum.photos/800/400"  # ВРЕМЕННАЯ заглушка

    await message.answer_photo(
        photo=photo_url,
        caption="",  # без текста, только фото + кнопка
        reply_markup=start_keyboard,
    )


@router.callback_query(F.data == "start_learning")
async def on_start_learning(callback: CallbackQuery):
    """
    Старт обучения: простой запрос в backend /ai/chat с ролью teacher.
    Здесь позже появится логика выбора курса, оплаты и т.д.
    """
    user_first_name = callback.from_user.first_name or "друг"

    prompt = (
        f"Поприветствуй пользователя по имени {user_first_name} и коротко объясни, "
        f"как устроена фабрика чат-курсов ChatCourseFactory. Скажи, что дальше он "
        f"сможет выбрать курс, оплатить в TON и пройти обучение прямо в этом чате."
    )

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{BACKEND_BASE_URL}/ai/chat",
            json={"role": "teacher", "prompt": prompt},
        )
        resp.raise_for_status()
        data = resp.json()

    reply_text = data.get("reply", "").strip() or "Что-то пошло не так, попробуйте ещё раз."

    await callback.message.answer(reply_text)
    await callback.answer()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
