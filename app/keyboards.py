from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

ADD_TASK = "➕ Add Task"
MY_TASKS = "📋 My Tasks"
COMPLETE_TASK = "✅ Complete Task"

def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ADD_TASK)],
            [KeyboardButton(text=MY_TASKS)],
            [KeyboardButton(text=COMPLETE_TASK)],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Choose an action",
    )
