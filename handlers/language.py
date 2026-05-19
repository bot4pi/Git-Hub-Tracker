from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import database as db
from config import BOT_TOKEN
from emoji_ids import e, DUCK_CHECK
from i18n import t
from keyboards import send_message, kb_language, kb_main_menu

router = Router(name="language")


@router.message(Command("language"))
@router.message(Command("lang"))
async def cmd_language(message: Message) -> None:
    lang = await db.resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await send_message(
        BOT_TOKEN,
        message.chat.id,
        t("language_choose", lang),
        keyboard=kb_language(),
    )


@router.callback_query(F.data.startswith("lang:"))
async def cb_set_language(callback: CallbackQuery) -> None:
    _, _, code = callback.data.partition(":")
    if code not in ("ru", "en"):
        await callback.answer()
        return

    await db.set_user_lang(callback.from_user.id, code)
    await callback.answer()

    key = "language_set_ru" if code == "ru" else "language_set_en"
    await send_message(
        BOT_TOKEN,
        callback.message.chat.id,
        t(key, code, check=e(DUCK_CHECK)),
        keyboard=kb_main_menu(code),
    )
