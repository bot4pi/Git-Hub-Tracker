import asyncio
import logging

from aiogram.exceptions import TelegramForbiddenError

import database as db
from config import BOT_TOKEN, CHECK_INTERVAL
from formatter import (
    format_org_events_report,
    format_repo_report,
    format_single_commit,
    format_user_events_report,
)
from github_client import (
    fetch_commit_detail,
    fetch_compare,
    fetch_latest_commit,
    fetch_org_events,
    fetch_user_events,
)
from keyboards import send_message

logger = logging.getLogger(__name__)

REQUEST_DELAY = 0.5


async def _safe_send(user_id: int, text: str) -> bool:
    """Отправить текст. При блокировке бота — удалить все записи юзера."""
    result = await send_message(BOT_TOKEN, user_id, text)
    if not result.get("ok"):
        desc = (result.get("description") or "").lower()
        code = result.get("error_code")
        if code == 403 or "blocked" in desc or "forbidden" in desc:
            logger.info("Бот заблокирован пользователем %s — чистим записи", user_id)
            await db.purge_user(user_id)
            return False
    return True


async def _user_lang(user_id: int) -> str:
    return await db.resolve_user_lang(user_id, None)


async def _check_repo(item: dict) -> None:
    user_id = item["user_id"]
    owner = item["owner"]
    repo = item["repo_name"]
    last_sha = item["last_sha"]

    latest = await fetch_latest_commit(owner, repo)
    if not latest:
        return
    latest_sha = latest.get("sha")
    if not latest_sha:
        return

    if not last_sha:
        await db.update_repo_sha(item["id"], latest_sha)
        return

    if latest_sha == last_sha:
        return

    lang = await _user_lang(user_id)
    compare = await fetch_compare(owner, repo, last_sha, latest_sha)
    text = None
    if compare and (compare.get("commits") or compare.get("files")):
        text = format_repo_report(owner, repo, compare, lang=lang)
    else:
        detail = await fetch_commit_detail(owner, repo, latest_sha)
        if detail:
            text = format_single_commit(owner, repo, detail, lang=lang)

    if text:
        await _safe_send(user_id, text)

    await db.update_repo_sha(item["id"], latest_sha)


def _new_events(events: list[dict], last_event_id: str) -> list[dict]:
    out = []
    for ev in events:
        if ev.get("id") == last_event_id:
            break
        out.append(ev)
    return out


async def _check_github_user(item: dict) -> None:
    user_id = item["user_id"]
    login = item["github_login"]
    last_event_id = item["last_event_id"]

    events = await fetch_user_events(login)
    if not events:
        return
    latest_id = events[0].get("id")
    if not latest_id:
        return

    if not last_event_id:
        await db.update_github_user_event(item["id"], latest_id)
        return

    if latest_id == last_event_id:
        return

    new_events = _new_events(events, last_event_id)
    if new_events:
        lang = await _user_lang(user_id)
        text = format_user_events_report(login, new_events, lang=lang)
        if text:
            await _safe_send(user_id, text)

    await db.update_github_user_event(item["id"], latest_id)


async def _check_org(item: dict) -> None:
    user_id = item["user_id"]
    login = item["org_login"]
    last_event_id = item["last_event_id"]

    events = await fetch_org_events(login)
    if not events:
        return
    latest_id = events[0].get("id")
    if not latest_id:
        return

    if not last_event_id:
        await db.update_org_event(item["id"], latest_id)
        return

    if latest_id == last_event_id:
        return

    new_events = _new_events(events, last_event_id)
    if new_events:
        lang = await _user_lang(user_id)
        text = format_org_events_report(login, new_events, lang=lang)
        if text:
            await _safe_send(user_id, text)

    await db.update_org_event(item["id"], latest_id)


async def run_check_cycle() -> None:
    logger.info("Старт проверки")
    try:
        repos = await db.get_all_repos()
    except Exception:
        logger.exception("Не удалось получить repos")
        repos = []
    for r in repos:
        try:
            await _check_repo(r)
        except Exception:
            logger.exception("Ошибка в проверке репо %s/%s", r.get("owner"), r.get("repo_name"))
        await asyncio.sleep(REQUEST_DELAY)

    try:
        users = await db.get_all_github_users()
    except Exception:
        logger.exception("Не удалось получить github_users")
        users = []
    for u in users:
        try:
            await _check_github_user(u)
        except Exception:
            logger.exception("Ошибка в проверке юзера %s", u.get("github_login"))
        await asyncio.sleep(REQUEST_DELAY)

    try:
        orgs = await db.get_all_orgs()
    except Exception:
        logger.exception("Не удалось получить orgs")
        orgs = []
    for o in orgs:
        try:
            await _check_org(o)
        except Exception:
            logger.exception("Ошибка в проверке орги %s", o.get("org_login"))
        await asyncio.sleep(REQUEST_DELAY)

    logger.info("Проверка завершена: репо=%d, юзеры=%d, орги=%d", len(repos), len(users), len(orgs))


def setup_scheduler(scheduler) -> None:
    scheduler.add_job(
        run_check_cycle,
        trigger="interval",
        seconds=CHECK_INTERVAL,
        next_run_time=None,
        id="check_cycle",
        max_instances=1,
        coalesce=True,
    )
