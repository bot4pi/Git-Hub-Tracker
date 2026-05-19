import re

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import database as db
from config import BOT_TOKEN
from emoji_ids import e, DUCK_CHECK, DUCK_TRASH, DUCK_PERSON, DUCK_SEARCH
from formatter import esc
from github_client import fetch_user_events, github_user_exists
from i18n import t
from keyboards import send_message, kb_after_add, kb_after_remove

router = Router(name="users")

_LOGIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")


def _clean_login(arg: str) -> str:
    arg = arg.strip().lstrip("@")
    if arg.startswith("https://github.com/"):
        arg = arg[len("https://github.com/") :].rstrip("/")
    return arg


def _emoji_kwargs() -> dict:
    return {
        "check":  e(DUCK_CHECK),
        "trash":  e(DUCK_TRASH),
        "person": e(DUCK_PERSON),
        "search": e(DUCK_SEARCH),
    }


@router.message(Command("adduser"))
async def cmd_adduser(message: Message, command: CommandObject) -> None:
    lang = await db.resolve_user_lang(message.from_user.id, message.from_user.language_code)
    em = _emoji_kwargs()

    arg = _clean_login(command.args or "")
    if not arg or not _LOGIN_RE.match(arg):
        await send_message(BOT_TOKEN, message.chat.id, t("adduser_bad_format", lang, **em))
        return

    if not await github_user_exists(arg):
        await send_message(
            BOT_TOKEN,
            message.chat.id,
            t("adduser_not_found", lang, login=esc(arg), **em),
        )
        return

    # Seed last_event_id, чтобы события, появившиеся между /adduser и тиком,
    # не пропустились.
    events = await fetch_user_events(arg)
    seed_event = events[0]["id"] if events else None

    ok = await db.add_github_user(message.from_user.id, arg, last_event_id=seed_event)
    if not ok:
        await send_message(
            BOT_TOKEN,
            message.chat.id,
            t("adduser_already", lang, login=esc(arg), **em),
            keyboard=kb_after_add(lang),
        )
        return

    await send_message(
        BOT_TOKEN,
        message.chat.id,
        t("adduser_added", lang, login=esc(arg), **em),
        keyboard=kb_after_add(lang),
    )


@router.message(Command("removeuser"))
async def cmd_removeuser(message: Message, command: CommandObject) -> None:
    lang = await db.resolve_user_lang(message.from_user.id, message.from_user.language_code)
    em = _emoji_kwargs()

    arg = _clean_login(command.args or "")
    if not arg:
        await send_message(BOT_TOKEN, message.chat.id, t("removeuser_specify", lang, **em))
        return

    ok = await db.remove_github_user(message.from_user.id, arg)
    if not ok:
        await send_message(
            BOT_TOKEN,
            message.chat.id,
            t("removeuser_not_in_list", lang, login=esc(arg), **em),
            keyboard=kb_after_remove(lang),
        )
        return

    await send_message(
        BOT_TOKEN,
        message.chat.id,
        t("removeuser_removed", lang, login=esc(arg), **em),
        keyboard=kb_after_remove(lang),
    )
