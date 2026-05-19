from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import database as db
from config import BOT_TOKEN, CHECK_INTERVAL
from emoji_ids import (
    e,
    DUCK_LIST,
    DUCK_LAPTOP,
    DUCK_PERSON,
    DUCK_BUILDING,
    DUCK_SEARCH,
)
from formatter import esc
from i18n import t
from keyboards import send_message, kb_empty_list, kb_after_add

router = Router(name="watchlist")


async def _render_list(user_id: int, lang: str) -> tuple[str, list]:
    repos = await db.get_user_repos(user_id)
    users = await db.get_user_github_users(user_id)
    orgs = await db.get_user_orgs(user_id)

    if not repos and not users and not orgs:
        return t("list_empty", lang, search=e(DUCK_SEARCH)), kb_empty_list(lang)

    lines = [t("list_title", lang, list=e(DUCK_LIST)), ""]

    if repos:
        lines.append(t("list_section_repos", lang, laptop=e(DUCK_LAPTOP), count=len(repos)))
        for r in repos:
            owner = esc(r["owner"])
            name = esc(r["repo_name"])
            url = esc(r["repo_url"])
            lines.append(f'  • <a href="{url}">{owner}/{name}</a>')
        lines.append("")

    if users:
        lines.append(t("list_section_users", lang, person=e(DUCK_PERSON), count=len(users)))
        for u in users:
            login = esc(u["github_login"])
            lines.append(f'  • <a href="https://github.com/{login}">{login}</a>')
        lines.append("")

    if orgs:
        lines.append(t("list_section_orgs", lang, building=e(DUCK_BUILDING), count=len(orgs)))
        for o in orgs:
            login = esc(o["org_login"])
            lines.append(f'  • <a href="https://github.com/{login}">{login}</a>')
        lines.append("")

    minutes = max(1, CHECK_INTERVAL // 60)
    lines.append(t("list_next_check", lang, minutes=minutes))

    return "\n".join(lines), kb_after_add(lang)


@router.message(Command("list"))
async def cmd_list(message: Message) -> None:
    lang = await db.resolve_user_lang(message.from_user.id, message.from_user.language_code)
    text, kb = await _render_list(message.from_user.id, lang)
    await send_message(BOT_TOKEN, message.chat.id, text, keyboard=kb)


@router.callback_query(F.data == "menu:list")
async def cb_list(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = await db.resolve_user_lang(callback.from_user.id, callback.from_user.language_code)
    text, kb = await _render_list(callback.from_user.id, lang)
    await send_message(BOT_TOKEN, callback.message.chat.id, text, keyboard=kb)
