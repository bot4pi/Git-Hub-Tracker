# Анимированные Duck Emoji (Telegram Premium)
# ВАЖНО: значения ниже — заглушки-примеры.
# Реальные ID нужно получить одним из способов:
#   1. Переслать анимированный duck стикер боту → прочитать sticker.custom_emoji_id
#   2. Использовать @getidsbot или @RawDataBot
#   3. GET /getCustomEmojiStickers с известными ID
# Duck стикерпак: https://t.me/addstickers/UtyaDuck или поиск "duck" в Premium emoji

DUCK_WAVE      = "5361542057048572613"   # утка машет — /start, приветствие
DUCK_LAPTOP    = "5359785904535761920"   # утка за ноутбуком — репозитории
DUCK_BELL      = "5373026167722876724"   # утка с колокольчиком — уведомление
DUCK_SEARCH    = "5373154152875294722"   # утка с лупой — мониторинг
DUCK_CHECK     = "5373154939432741888"   # утка с галочкой — успешное действие
DUCK_TRASH     = "5373233173264117634"   # утка с мусорным ведром — удаление
DUCK_LIST      = "5373080822371614159"   # утка со списком — /list
DUCK_PERSON    = "5373067291984011402"   # утка-персона — GitHub пользователи
DUCK_BUILDING  = "5373055698587091059"   # утка со зданием — организации
DUCK_FIRE      = "5373183862251220128"   # утка с огнём — активность
DUCK_PLUS      = "5373210748521677682"   # утка с плюсом — добавить

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
}


import os

# Если есть Premium у владельца бота и заполнены реальные ID — включить.
# По умолчанию выключено: ID в этом файле — заглушки, Telegram отдаёт
# DOCUMENT_INVALID если ID не существует.
USE_CUSTOM_EMOJI = os.getenv("USE_CUSTOM_EMOJI", "0") == "1"


def e(emoji_id: str) -> str:
    """Вернуть кастомный emoji (если включено) или fallback-символ."""
    fallback = FALLBACK.get(emoji_id, "•")
    if not USE_CUSTOM_EMOJI:
        return fallback
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
