import logging
import re
from typing import Optional

import aiohttp

from config import GITHUB_TOKEN

logger = logging.getLogger(__name__)

API_BASE = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "github-tracker-bot",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


_REPO_URL_RE = re.compile(
    r"^(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)
_OWNER_REPO_RE = re.compile(r"^([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$")


def parse_repo_url(url: str) -> Optional[tuple[str, str]]:
    """
    Парсит URL → (owner, repo).
    Поддерживает: github.com/o/r, https://github.com/o/r, https://github.com/o/r.git, o/r.
    """
    if not url:
        return None
    url = url.strip()
    m = _REPO_URL_RE.match(url)
    if m:
        return m.group(1), m.group(2)
    m = _OWNER_REPO_RE.match(url)
    if m:
        return m.group(1), m.group(2)
    return None


async def _get_json(session: aiohttp.ClientSession, url: str, params: Optional[dict] = None):
    try:
        async with session.get(url, headers=HEADERS, params=params, timeout=aiohttp.ClientTimeout(total=20)) as resp:
            if resp.status in (403, 429):
                remaining = resp.headers.get("X-RateLimit-Remaining")
                reset = resp.headers.get("X-RateLimit-Reset")
                logger.warning("GitHub rate limit: %s (remaining=%s, reset=%s)", url, remaining, reset)
                return None, resp.status
            if resp.status == 404:
                return None, 404
            if resp.status >= 400:
                logger.warning("GitHub %s → %s", url, resp.status)
                return None, resp.status
            return await resp.json(), resp.status
    except Exception as ex:
        logger.exception("GitHub request failed %s: %s", url, ex)
        return None, 0


async def repo_exists(owner: str, repo: str) -> bool:
    async with aiohttp.ClientSession() as s:
        data, status = await _get_json(s, f"{API_BASE}/repos/{owner}/{repo}")
        return data is not None and status == 200


async def github_user_exists(login: str) -> bool:
    """True если это именно пользователь (не организация)."""
    async with aiohttp.ClientSession() as s:
        data, _ = await _get_json(s, f"{API_BASE}/users/{login}")
        if not data:
            return False
        return data.get("type") == "User"


async def org_exists(login: str) -> bool:
    async with aiohttp.ClientSession() as s:
        data, status = await _get_json(s, f"{API_BASE}/orgs/{login}")
        return data is not None and status == 200


async def fetch_latest_commit(owner: str, repo: str) -> Optional[dict]:
    async with aiohttp.ClientSession() as s:
        data, _ = await _get_json(s, f"{API_BASE}/repos/{owner}/{repo}/commits", params={"per_page": 1})
        if isinstance(data, list) and data:
            return data[0]
        return None


async def fetch_compare(owner: str, repo: str, base: str, head: str) -> Optional[dict]:
    async with aiohttp.ClientSession() as s:
        data, _ = await _get_json(s, f"{API_BASE}/repos/{owner}/{repo}/compare/{base}...{head}")
        return data


async def fetch_commit_detail(owner: str, repo: str, sha: str) -> Optional[dict]:
    async with aiohttp.ClientSession() as s:
        data, _ = await _get_json(s, f"{API_BASE}/repos/{owner}/{repo}/commits/{sha}")
        return data


async def fetch_user_events(login: str) -> list[dict]:
    async with aiohttp.ClientSession() as s:
        data, _ = await _get_json(s, f"{API_BASE}/users/{login}/events/public", params={"per_page": 10})
        return data if isinstance(data, list) else []


async def fetch_org_events(login: str) -> list[dict]:
    async with aiohttp.ClientSession() as s:
        data, _ = await _get_json(s, f"{API_BASE}/orgs/{login}/events", params={"per_page": 10})
        return data if isinstance(data, list) else []
