import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from app.config import load_settings
from app.database import Database
from app.handlers import start, tasks, fallback

async def configure_bot(bot: Bot, settings) -> None:
    await bot.set_my_name(name=settings.bot_name)
    await bot.set_my_short_description(short_description=settings.bot_about)
    await bot.set_my_description(description=settings.bot_description)
    await bot.set_my_commands(
        [BotCommand(command="start", description="Open the main menu")]
    )

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    settings = load_settings()
    db = Database(settings.database_path)

    bot = Bot(
        settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp["settings"] = settings
    dp["db"] = db

    dp.include_router(start.router)
    dp.include_router(tasks.router)
    dp.include_router(fallback.router)

    await configure_bot(bot, settings)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
