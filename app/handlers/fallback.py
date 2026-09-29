from aiogram import F, Router
from aiogram.types import Message
from app.keyboards import main_keyboard

router = Router()

@router.message(F.text)
async def fallback_handler(message: Message):
    await message.answer(
        "I didn't recognize that input.\n\n"
        "Use one of the three buttons below, or send /start.",
        reply_markup=main_keyboard(),
    )
