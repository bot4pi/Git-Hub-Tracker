<h1 align="center">Git-Hub-Tracker</h1>

<p align="center">
  <a href="https://github.com/bot4pi"><img src="https://img.shields.io/badge/Author-bot4pi-89b4fa?style=for-the-badge&logo=github&logoColor=white&labelColor=302D41" alt="Author"></a>&nbsp;
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=FFD93B&labelColor=302D41" alt="Python"></a>&nbsp;
  <a href="https://docs.aiogram.dev/"><img src="https://img.shields.io/badge/aiogram-3.10-26A5E4?style=for-the-badge&logo=telegram&logoColor=white&labelColor=302D41" alt="aiogram"></a>&nbsp;
  <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/SQLite-aiosqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white&labelColor=302D41" alt="SQLite"></a>&nbsp;
  <a href="https://docs.github.com/rest"><img src="https://img.shields.io/badge/GitHub-API-CBA6F7?style=for-the-badge&logo=github&logoColor=white&labelColor=302D41" alt="GitHub API"></a>
</p>

---

### ✨ Описание

**Git-Hub-Tracker** — Telegram-бот на **aiogram 3** для отслеживания активности на GitHub.
Коммиты в репозиториях, активность пользователей, события организаций — всё прилетает прямо в чат с красивым UI и поддержкой кастомных эмодзи Telegram Premium.

Без AI и лишних абстракций: чистый GitHub REST API + SQLite + APScheduler.

---

### 🚀 Возможности

- 📦 **Репозитории** — уведомления о новых коммитах с diff'ом изменённых файлов
- 👤 **Пользователи** — мониторинг публичной активности (push, fork, star, release, issues, PR)
- 🏢 **Организации** — отслеживание событий орг-уровня
- 🌐 **i18n** — русский и английский, автоопределение по `language_code` Telegram
- 🦆 **Custom emoji** — анимированные duck-стикеры Telegram Premium (опционально)
- 🎨 **Цветные кнопки** — Bot API 9.4 (`style` + `icon_custom_emoji_id`)
- ⏱️ **AsyncIOScheduler** — периодическая проверка с настраиваемым интервалом

---

### 🛠️ Стек

<p align="left">
  <img src="https://skillicons.dev/icons?i=python,sqlite,git,github" />
</p>

**Framework:** aiogram 3.10
**Async HTTP:** aiohttp
**Database:** aiosqlite (SQLite)
**Scheduler:** APScheduler 3
**API:** GitHub REST `2022-11-28` + Telegram Bot API 9.4

---

## 📦 Установка

```bash
git clone https://github.com/bot4pi/Git-Hub-Tracker.git
cd Git-Hub-Tracker
pip install -r requirements.txt
```

## ⚙️ Конфигурация

Создай `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

| Переменная | Описание | По умолчанию |
|---|---|---|
| `BOT_TOKEN` | Токен Telegram-бота от [@BotFather](https://t.me/BotFather) | — |
| `GITHUB_TOKEN` | GitHub PAT (опционально, поднимает rate-limit с 60 до 5000 req/h) | — |
| `CHECK_INTERVAL` | Интервал проверки в секундах | `300` |
| `DB_PATH` | Путь к SQLite | `tracker.db` |
| `USE_CUSTOM_EMOJI` | `1` если у владельца бота есть Telegram Premium и заполнены реальные duck-ID в `emoji_ids.py` | `0` |

## ▶️ Запуск

```bash
python bot.py
```

---

### 💬 Команды

| Команда | Действие |
|---|---|
| `/start`, `/help` | Приветствие и главное меню |
| `/list` | Список того, что отслеживается |
| `/addrepo <url>` | Добавить репозиторий |
| `/removerepo <owner/repo>` | Удалить репозиторий |
| `/adduser <login>` | Добавить пользователя GitHub |
| `/removeuser <login>` | Удалить пользователя |
| `/addorg <login>` | Добавить организацию |
| `/removeorg <login>` | Удалить организацию |
| `/language` | Переключить язык (RU ⇄ EN) |

---

### 📡 Обрабатываемые события GitHub

<p>
  <img src="https://img.shields.io/badge/PushEvent-a6e3a1?style=flat-square&labelColor=302D41" alt="PushEvent">
  <img src="https://img.shields.io/badge/CreateEvent-94e2d5?style=flat-square&labelColor=302D41" alt="CreateEvent">
  <img src="https://img.shields.io/badge/ForkEvent-89dceb?style=flat-square&labelColor=302D41" alt="ForkEvent">
  <img src="https://img.shields.io/badge/WatchEvent-f9e2af?style=flat-square&labelColor=302D41" alt="WatchEvent">
  <img src="https://img.shields.io/badge/ReleaseEvent-fab387?style=flat-square&labelColor=302D41" alt="ReleaseEvent">
  <img src="https://img.shields.io/badge/IssuesEvent-f38ba8?style=flat-square&labelColor=302D41" alt="IssuesEvent">
  <img src="https://img.shields.io/badge/PullRequestEvent-cba6f7?style=flat-square&labelColor=302D41" alt="PullRequestEvent">
  <img src="https://img.shields.io/badge/PublicEvent-89b4fa?style=flat-square&labelColor=302D41" alt="PublicEvent">
</p>

---

### 🗂️ Структура

```
bot.py              · точка входа
config.py           · переменные окружения
database.py         · SQLite через aiosqlite
github_client.py    · запросы к GitHub API
scheduler.py        · периодическая проверка
formatter.py        · отчёты, экранирование, события
emoji_ids.py        · ID custom emoji + fallback
keyboards.py        · клавиатуры через прямой Bot API
i18n.py             · переводы RU/EN
handlers/           · /start, /addrepo, /adduser, /addorg, /list, /language
```

---

<p align="center">© 2026 bot4pi</p>
