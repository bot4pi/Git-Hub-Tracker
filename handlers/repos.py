from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import database as db
from config import BOT_TOKEN
from emoji_ids import e, DUCK_CHECK, DUCK_TRASH, DUCK_LAPTOP, DUCK_SEARCH
from formatter import esc
from github_client import parse_repo_url, repo_exists
from i18n import t
from keyboards import send_message, kb_after_add, kb_after_remove

router = Router(name="repos")


def _emoji_kwargs() -> dict:
    return {
        "check":  e(DUCK_CHECK),
        "trash":  e(DUCK_TRASH),
        "laptop": e(DUCK_LAPTOP),
        "search": e(DUCK_SEARCH),
    }


@router.message(Command("addrepo"))
async def cmd_addrepo(message: Message, command: CommandObject) -> None:
    lang = await db.resolve_user_lang(message.from_user.id, message.from_user.language_code)
    em = _emoji_kwargs()

    arg = (command.args or "").strip()
    if not arg:
        await send_message(BOT_TOKEN, message.chat.id, t("addrepo_bad_format", lang, **em))
        return

    parsed = parse_repo_url(arg)
    if not parsed:
        await send_message(BOT_TOKEN, message.chat.id, t("addrepo_bad_format", lang, **em))
        return

    owner, repo = parsed
    if not await repo_exists(owner, repo):
        await send_message(
            BOT_TOKEN,
            message.chat.id,
            t("addrepo_not_found", lang, owner=esc(owner), repo=esc(repo), **em),
        )
        return

    repo_url = f"https://github.com/{owner}/{repo}"
    ok = await db.add_repo(message.from_user.id, repo_url, owner, repo)
    if not ok:
        await send_message(
            BOT_TOKEN,
            message.chat.id,
            t("addrepo_already", lang, url=esc(repo_url), owner=esc(owner), repo=esc(repo), **em),
            keyboard=kb_after_add(lang),
        )
        return

    await send_message(
        BOT_TOKEN,
        message.chat.id,
        t("addrepo_added", lang, url=esc(repo_url), owner=esc(owner), repo=esc(repo), **em),
        keyboard=kb_after_add(lang),
    )


@router.message(Command("removerepo"))
async def cmd_removerepo(message: Message, command: CommandObject) -> None:
    lang = await db.resolve_user_lang(message.from_user.id, message.from_user.language_code)
    em = _emoji_kwargs()

    arg = (command.args or "").strip()
    if not arg:
        await send_message(BOT_TOKEN, message.chat.id, t("removerepo_specify", lang, **em))
        return

    parsed = parse_repo_url(arg)
    if not parsed:
        await send_message(BOT_TOKEN, message.chat.id, t("removerepo_bad_format", lang, **em))
        return

    owner, repo = parsed
    ok = await db.remove_repo(message.from_user.id, owner, repo)
    if not ok:
        await send_message(
            BOT_TOKEN,
            message.chat.id,
            t("removerepo_not_in_list", lang, owner=esc(owner), repo=esc(repo), **em),
            keyboard=kb_after_remove(lang),
        )
        return

    await send_message(
        BOT_TOKEN,
        message.chat.id,
        t("removerepo_removed", lang, owner=esc(owner), repo=esc(repo), **em),
        keyboard=kb_after_remove(lang),
    )
