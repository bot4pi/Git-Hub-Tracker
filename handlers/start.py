from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

import database as db
from config import BOT_TOKEN
from emoji_ids import (
    e,
    DUCK_WAVE,
    DUCK_LAPTOP,
    DUCK_PERSON,
    DUCK_BUILDING,
    DUCK_PLUS,
    DUCK_SEARCH,
)
from i18n import t, lang_for_user
from keyboards import send_message, kb_main_menu

router = Router(name="start")


def _emoji_kwargs() -> dict:
    return {
        "wave":     e(DUCK_WAVE),
        "laptop":   e(DUCK_LAPTOP),
        "person":   e(DUCK_PERSON),
        "building": e(DUCK_BUILDING),
        "plus":     e(DUCK_PLUS),
        "search":   e(DUCK_SEARCH),
    }


@router.message(CommandStart())
@router.message(Command("help"))
async def cmd_start(message: Message) -> None:
    # При первом /start сохраняем язык из Telegram, если ничего ещё не выбрано
    stored = await db.get_user_lang(message.from_user.id)
    lang = lang_for_user(stored, message.from_user.language_code)
    if stored is None:
        await db.set_user_lang(message.from_user.id, lang)

    await send_message(
        BOT_TOKEN,
        message.chat.id,
        t("welcome", lang, **_emoji_kwargs()),
        keyboard=kb_main_menu(lang),
    )


async def _resolve_lang(user) -> str:
    return await db.resolve_user_lang(user.id, user.language_code)


@router.callback_query(F.data == "menu:add_more")
async def cb_add_more(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = await _resolve_lang(callback.from_user)
    await send_message(
        BOT_TOKEN,
        callback.message.chat.id,
        t("add_hint", lang, **_emoji_kwargs()),
        keyboard=kb_main_menu(lang),
    )


@router.callback_query(F.data == "menu:add_repo")
async def cb_add_repo(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = await _resolve_lang(callback.from_user)
    await send_message(BOT_TOKEN, callback.message.chat.id, t("menu_add_repo_text", lang, **_emoji_kwargs()))


@router.callback_query(F.data == "menu:add_user")
async def cb_add_user(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = await _resolve_lang(callback.from_user)
    await send_message(BOT_TOKEN, callback.message.chat.id, t("menu_add_user_text", lang, **_emoji_kwargs()))


@router.callback_query(F.data == "menu:add_org")
async def cb_add_org(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = await _resolve_lang(callback.from_user)
    await send_message(BOT_TOKEN, callback.message.chat.id, t("menu_add_org_text", lang, **_emoji_kwargs()))


@router.callback_query(F.data == "menu:repos")
async def cb_repos(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = await _resolve_lang(callback.from_user)
    await send_message(BOT_TOKEN, callback.message.chat.id, t("menu_repos_text", lang, **_emoji_kwargs()))


@router.callback_query(F.data == "menu:users")
async def cb_users(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = await _resolve_lang(callback.from_user)
    await send_message(BOT_TOKEN, callback.message.chat.id, t("menu_users_text", lang, **_emoji_kwargs()))


@router.callback_query(F.data == "menu:orgs")
async def cb_orgs(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = await _resolve_lang(callback.from_user)
    await send_message(BOT_TOKEN, callback.message.chat.id, t("menu_orgs_text", lang, **_emoji_kwargs()))
