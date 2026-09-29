from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.database import Database
from app.keyboards import ADD_TASK, MY_TASKS, COMPLETE_TASK, main_keyboard

router = Router()

class TaskStates(StatesGroup):
    waiting_for_task = State()

def complete_keyboard(task_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Mark as completed", callback_data=f"complete:{task_id}")]
        ]
    )

@router.message(F.text == ADD_TASK)
async def add_task_start(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_task)
    await message.answer(
        "Send the task you want to add.\n\nExample: Finish the project report",
        reply_markup=main_keyboard(),
    )

@router.message(TaskStates.waiting_for_task)
async def add_task_save(message: Message, state: FSMContext, db: Database):
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send the task as text.")
        return
    if text.startswith("/"):
        await message.answer("Please enter the task text, or use /start to open the main menu.")
        return
    if len(text) > 500:
        await message.answer("Please keep the task under 500 characters.")
        return

    await db.add_task(message.from_user.id, text)
    await state.clear()
    await message.answer(f"✅ Task added:\n\n• {text}", reply_markup=main_keyboard())

@router.message(F.text == MY_TASKS)
async def show_tasks(message: Message, db: Database):
    tasks = await db.list_tasks(message.from_user.id)
    if not tasks:
        await message.answer(
            "You have no active tasks.\n\nTap “➕ Add Task” to create one.",
            reply_markup=main_keyboard(),
        )
        return

    lines = ["📋 Your active tasks:\n"] + [f"{i}. {t.text}" for i, t in enumerate(tasks, 1)]
    await message.answer("\n".join(lines), reply_markup=main_keyboard())

@router.message(F.text == COMPLETE_TASK)
async def choose_task(message: Message, db: Database):
    tasks = await db.list_tasks(message.from_user.id)
    if not tasks:
        await message.answer(
            "There are no active tasks to complete.",
            reply_markup=main_keyboard(),
        )
        return

    await message.answer("Select the task you want to complete:", reply_markup=main_keyboard())
    for task in tasks:
        await message.answer(
            f"• {task.text}",
            reply_markup=complete_keyboard(task.id),
        )

@router.callback_query(F.data.startswith("complete:"))
async def complete_task(callback: CallbackQuery, db: Database):
    try:
        task_id = int(callback.data.split(":", 1)[1])
    except (ValueError, AttributeError):
        await callback.answer("Invalid task.", show_alert=True)
        return

    if not await db.complete_task(callback.from_user.id, task_id):
        await callback.answer("Task is already completed or no longer exists.", show_alert=True)
        return

    await callback.answer("Task completed.")
    if callback.message:
        await callback.message.edit_text("✅ Task completed.")
