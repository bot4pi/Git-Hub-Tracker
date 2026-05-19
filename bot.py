import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN
from database import init_db
from handlers import setup_routers
from i18n import t
from scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


_COMMAND_KEYS = [
    ("start",      "cmd_start"),
    ("help",       "cmd_help"),
    ("list",       "cmd_list"),
    ("addrepo",    "cmd_addrepo"),
    ("removerepo", "cmd_removerepo"),
    ("adduser",    "cmd_adduser"),
    ("removeuser", "cmd_removeuser"),
    ("addorg",     "cmd_addorg"),
    ("removeorg",  "cmd_removeorg"),
    ("language",   "cmd_language"),
]


def _commands_for(lang: str) -> list[BotCommand]:
    return [BotCommand(command=cmd, description=t(key, lang)) for cmd, key in _COMMAND_KEYS]


async def _set_bot_commands(bot: Bot) -> None:
    # Русский — дефолт (для всех остальных language_code)
    await bot.set_my_commands(_commands_for("ru"), scope=BotCommandScopeDefault())
    # Английский — для пользователей с language_code='en'
    await bot.set_my_commands(_commands_for("en"), scope=BotCommandScopeDefault(), language_code="en")


async def main() -> None:
    await init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(setup_routers())

    await _set_bot_commands(bot)

    scheduler = AsyncIOScheduler()
    setup_scheduler(scheduler)
    scheduler.start()

    me = await bot.get_me()
    logger.info("Бот запущен: @%s (id=%s)", me.username, me.id)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Остановка")
