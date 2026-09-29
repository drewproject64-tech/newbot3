from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.keyboards import main_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, settings) -> None:
    await message.answer(
        f"Welcome to {settings.bot_name}.\n\n"
        "Manage your personal task list directly in Telegram.\n\n"
        "Use the three buttons below to add tasks, view active tasks, "
        "or mark a task as completed.",
        reply_markup=main_keyboard(),
    )
