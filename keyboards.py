import json
import logging
from typing import Optional

import aiohttp

from emoji_ids import (
    DUCK_LAPTOP,
    DUCK_PERSON,
    DUCK_BUILDING,
    DUCK_LIST,
    DUCK_PLUS,
    DUCK_TRASH,
)
from i18n import t

logger = logging.getLogger(__name__)

API_BASE = "https://api.telegram.org/bot{token}/{method}"


def btn(text: str, callback: str, style: Optional[str] = None, icon_id: Optional[str] = None) -> dict:
    """Собрать объект кнопки. style: primary|success|danger."""
    b = {"text": text, "callback_data": callback}
    if style:
        b["style"] = style
    if icon_id:
        b["icon_custom_emoji_id"] = icon_id
    return b


def url_btn(text: str, url: str, icon_id: Optional[str] = None) -> dict:
    b = {"text": text, "url": url}
    if icon_id:
        b["icon_custom_emoji_id"] = icon_id
    return b


async def send_message(
    bot_token: str,
    chat_id: int,
    text: str,
    keyboard: Optional[list] = None,
    edit_message_id: Optional[int] = None,
    disable_web_page_preview: bool = True,
) -> dict:
    """
    Отправить или отредактировать сообщение с цветными кнопками через прямой Bot API.
    keyboard — список строк, каждая строка — список объектов кнопок.
    """
    method = "editMessageText" if edit_message_id else "sendMessage"
    url = API_BASE.format(token=bot_token, method=method)
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true" if disable_web_page_preview else "false",
    }
    if keyboard is not None:
        payload["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    if edit_message_id:
        payload["message_id"] = edit_message_id

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                data = await resp.json()
                if not data.get("ok"):
                    logger.warning("Bot API %s failed: %s", method, data)
                return data
    except Exception as ex:
        logger.exception("Bot API request error: %s", ex)
        return {"ok": False, "error": str(ex)}


# Готовые наборы кнопок ---------------------------------------------------

def kb_main_menu(lang: str = "ru") -> list:
    return [
        [
            btn(t("btn_repos", lang), "menu:repos", style="primary", icon_id=DUCK_LAPTOP),
            btn(t("btn_users", lang), "menu:users", style="primary", icon_id=DUCK_PERSON),
            btn(t("btn_orgs", lang),  "menu:orgs",  style="primary", icon_id=DUCK_BUILDING),
        ],
        [btn(t("btn_list", lang), "menu:list", style="primary", icon_id=DUCK_LIST)],
    ]


def kb_after_add(lang: str = "ru") -> list:
    return [
        [
            btn(t("btn_list", lang), "menu:list", style="primary", icon_id=DUCK_LIST),
            btn(t("btn_add_more", lang), "menu:add_more", icon_id=DUCK_PLUS),
        ]
    ]


def kb_after_remove(lang: str = "ru") -> list:
    return [
        [
            btn(t("btn_list", lang), "menu:list", style="primary", icon_id=DUCK_LIST),
        ]
    ]


def kb_empty_list(lang: str = "ru") -> list:
    return [
        [
            btn(t("btn_add_repo", lang), "menu:add_repo", style="success", icon_id=DUCK_LAPTOP),
            btn(t("btn_add_user", lang), "menu:add_user", style="success", icon_id=DUCK_PERSON),
            btn(t("btn_add_org", lang),  "menu:add_org",  style="success", icon_id=DUCK_BUILDING),
        ]
    ]


def kb_language() -> list:
    return [
        [
            btn(t("btn_lang_ru", "ru"), "lang:ru", style="primary"),
            btn(t("btn_lang_en", "en"), "lang:en", style="primary"),
        ]
    ]
