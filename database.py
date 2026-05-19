import logging
from typing import Optional

import aiosqlite

from config import DB_PATH

logger = logging.getLogger(__name__)


SCHEMA = """
CREATE TABLE IF NOT EXISTS tracked_repos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    repo_url    TEXT    NOT NULL,
    owner       TEXT    NOT NULL,
    repo_name   TEXT    NOT NULL,
    last_sha    TEXT,
    added_at    TEXT    DEFAULT (datetime('now')),
    UNIQUE(user_id, owner, repo_name)
);

CREATE TABLE IF NOT EXISTS tracked_github_users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    github_login    TEXT    NOT NULL,
    last_event_id   TEXT,
    added_at        TEXT    DEFAULT (datetime('now')),
    UNIQUE(user_id, github_login)
);

CREATE TABLE IF NOT EXISTS tracked_orgs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    org_login       TEXT    NOT NULL,
    last_event_id   TEXT,
    added_at        TEXT    DEFAULT (datetime('now')),
    UNIQUE(user_id, org_login)
);

CREATE TABLE IF NOT EXISTS user_settings (
    user_id     INTEGER PRIMARY KEY,
    lang        TEXT    NOT NULL DEFAULT 'ru',
    updated_at  TEXT    DEFAULT (datetime('now'))
);
"""


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


# --- Репозитории --------------------------------------------------------

async def add_repo(user_id: int, repo_url: str, owner: str, repo_name: str) -> bool:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO tracked_repos (user_id, repo_url, owner, repo_name) VALUES (?, ?, ?, ?)",
                (user_id, repo_url, owner.lower(), repo_name.lower()),
            )
            await db.commit()
        return True
    except aiosqlite.IntegrityError:
        return False


async def remove_repo(user_id: int, owner: str, repo_name: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM tracked_repos WHERE user_id = ? AND owner = ? AND repo_name = ?",
            (user_id, owner.lower(), repo_name.lower()),
        )
        await db.commit()
        return cur.rowcount > 0


async def get_user_repos(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, repo_url, owner, repo_name, last_sha FROM tracked_repos WHERE user_id = ? ORDER BY id",
            (user_id,),
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def get_all_repos() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, user_id, repo_url, owner, repo_name, last_sha FROM tracked_repos ORDER BY id"
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def update_repo_sha(repo_id: int, sha: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE tracked_repos SET last_sha = ? WHERE id = ?", (sha, repo_id))
        await db.commit()


# --- GitHub пользователи ------------------------------------------------

async def add_github_user(user_id: int, github_login: str) -> bool:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO tracked_github_users (user_id, github_login) VALUES (?, ?)",
                (user_id, github_login.lower()),
            )
            await db.commit()
        return True
    except aiosqlite.IntegrityError:
        return False


async def remove_github_user(user_id: int, github_login: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM tracked_github_users WHERE user_id = ? AND github_login = ?",
            (user_id, github_login.lower()),
        )
        await db.commit()
        return cur.rowcount > 0


async def get_user_github_users(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, github_login, last_event_id FROM tracked_github_users WHERE user_id = ? ORDER BY id",
            (user_id,),
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def get_all_github_users() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, user_id, github_login, last_event_id FROM tracked_github_users ORDER BY id"
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def update_github_user_event(tracked_id: int, event_id: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE tracked_github_users SET last_event_id = ? WHERE id = ?",
            (event_id, tracked_id),
        )
        await db.commit()


# --- Организации -------------------------------------------------------

async def add_org(user_id: int, org_login: str) -> bool:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO tracked_orgs (user_id, org_login) VALUES (?, ?)",
                (user_id, org_login.lower()),
            )
            await db.commit()
        return True
    except aiosqlite.IntegrityError:
        return False


async def remove_org(user_id: int, org_login: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM tracked_orgs WHERE user_id = ? AND org_login = ?",
            (user_id, org_login.lower()),
        )
        await db.commit()
        return cur.rowcount > 0


async def get_user_orgs(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, org_login, last_event_id FROM tracked_orgs WHERE user_id = ? ORDER BY id",
            (user_id,),
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def get_all_orgs() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, user_id, org_login, last_event_id FROM tracked_orgs ORDER BY id"
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def update_org_event(tracked_id: int, event_id: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE tracked_orgs SET last_event_id = ? WHERE id = ?",
            (event_id, tracked_id),
        )
        await db.commit()


# --- Удаление всех записей пользователя (при блокировке бота) ----------

async def purge_user(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM tracked_repos WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM tracked_github_users WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM tracked_orgs WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM user_settings WHERE user_id = ?", (user_id,))
        await db.commit()
        logger.info("Удалены все записи пользователя %s", user_id)


# --- Настройки пользователя (язык) -------------------------------------

async def get_user_lang(user_id: int) -> Optional[str]:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT lang FROM user_settings WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else None


async def set_user_lang(user_id: int, lang: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO user_settings (user_id, lang) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET lang = excluded.lang, updated_at = datetime('now')",
            (user_id, lang),
        )
        await db.commit()


async def resolve_user_lang(user_id: int, telegram_lang_code: Optional[str]) -> str:
    """Выбрать язык пользователя: сохранённый в БД, либо из Telegram."""
    from i18n import lang_for_user

    stored = await get_user_lang(user_id)
    return lang_for_user(stored, telegram_lang_code)
