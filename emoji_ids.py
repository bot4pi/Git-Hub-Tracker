import os

# Анимированные Duck Emoji (Telegram Premium)
# ID получены из стикерпака UtyaDuck.
# Включается флагом USE_CUSTOM_EMOJI=1 в .env (требует Premium у владельца бота).

DUCK_WAVE      = "5357394101673140791"   # утка машет — /start, приветствие
DUCK_LAPTOP    = "5444965061749644170"   # утка за ноутбуком — репозитории
DUCK_BELL      = "5974287633151432130"   # утка с колокольчиком — уведомление
DUCK_SEARCH    = "5305243423354134165"   # утка с лупой — мониторинг
DUCK_CHECK     = "5429106552139173716"   # утка с галочкой — успешное действие
DUCK_TRASH     = "5766889228705205205"   # утка с мусорным ведром — удаление
DUCK_LIST      = "5897705437096055739"   # утка со списком — /list
DUCK_PERSON    = "5895288332581082241"   # утка-персона — GitHub пользователи
DUCK_BUILDING  = "5861643186576825694"   # утка со зданием — организации
DUCK_FIRE      = "5789605753115384004"   # утка с огнём — активность
DUCK_PLUS      = "5397916757333654639"   # утка с плюсом — добавить
DUCK_WATCH     = "6050887597486513073"   # утка с часами — дата/время

FALLBACK = {
    DUCK_WAVE:     "👋",
    DUCK_LAPTOP:   "💻",
    DUCK_BELL:     "🔔",
    DUCK_SEARCH:   "🔍",
    DUCK_CHECK:    "✅",
    DUCK_TRASH:    "🗑",
    DUCK_LIST:     "📋",
    DUCK_PERSON:   "👤",
    DUCK_BUILDING: "🏢",
    DUCK_FIRE:     "🔥",
    DUCK_PLUS:     "➕",
    DUCK_WATCH:    "🕐",
}


# Если есть Premium у владельца бота и заполнены реальные ID — включить.
# По умолчанию выключено: при невалидных ID Telegram отдаёт DOCUMENT_INVALID
# и рушит всё сообщение целиком.
USE_CUSTOM_EMOJI = os.getenv("USE_CUSTOM_EMOJI", "0") == "1"


def e(emoji_id: str) -> str:
    """Вернуть кастомный emoji (если включено) или fallback-символ."""
    fallback = FALLBACK.get(emoji_id, "•")
    if not USE_CUSTOM_EMOJI:
        return fallback
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
