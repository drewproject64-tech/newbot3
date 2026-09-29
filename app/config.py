import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    bot_token: str
    bot_name: str = "SB24 ToDo List Bot"
    bot_username: str = "@SB24ToDoBot"
    bot_about: str = "Simple Telegram task list for adding, viewing, and completing tasks."
    bot_description: str = "SB24 ToDo List Bot helps you manage a personal task list directly in Telegram. Add tasks, view your current tasks, and mark completed tasks without leaving Telegram."
    database_path: str = "data/todo.db"

def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN","").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required.")
    return Settings(
        bot_token=token,
        bot_name=os.getenv("BOT_NAME","SB24 ToDo List Bot"),
        bot_username=os.getenv("BOT_USERNAME","@SB24ToDoBot"),
        bot_about=os.getenv("BOT_ABOUT","Simple Telegram task list for adding, viewing, and completing tasks."),
        bot_description=os.getenv("BOT_DESCRIPTION","SB24 ToDo List Bot helps you manage a personal task list directly in Telegram. Add tasks, view your current tasks, and mark completed tasks without leaving Telegram."),
        database_path=os.getenv("DATABASE_PATH","data/todo.db"),
    )
