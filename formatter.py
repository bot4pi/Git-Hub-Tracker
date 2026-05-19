from datetime import datetime
from typing import Optional

from emoji_ids import (
    e,
    DUCK_BELL,
    DUCK_LAPTOP,
    DUCK_FIRE,
    DUCK_PERSON,
    DUCK_BUILDING,
    DUCK_CHECK,
    DUCK_WATCH,
)
from i18n import t

MAX_COMMITS = 5
MAX_FILES = 15
MAX_EVENTS = 5

STATUS_ICONS = {
    "added": "🟢",
    "removed": "🔴",
    "modified": "🟡",
    "renamed": "🔵",
}


def esc(s: Optional[str]) -> str:
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _fmt_iso(ts: Optional[str]) -> str:
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M UTC")
    except Exception:
        return esc(ts)


def _short_msg(msg: str, limit: int = 100) -> str:
    msg = (msg or "").split("\n", 1)[0].strip()
    if len(msg) > limit:
        msg = msg[: limit - 1].rstrip() + "…"
    return msg


def _author_label(lang: str) -> str:
    return "Author" if lang == "en" else "Автор"


def format_repo_report(owner: str, repo: str, compare: dict, lang: str = "ru") -> str:
    """Отчёт по новым коммитам в репозитории."""
    commits = compare.get("commits") or []
    files = compare.get("files") or []
    total = len(commits)

    lines = []
    lines.append(t("report_repo_update", lang, bell=e(DUCK_BELL)))
    lines.append(
        f'{e(DUCK_LAPTOP)} <a href="https://github.com/{esc(owner)}/{esc(repo)}">{esc(owner)}/{esc(repo)}</a>'
    )
    lines.append("")
    lines.append(t("report_new_commits", lang, fire=e(DUCK_FIRE), count=total))
    lines.append("")

    shown = commits[-MAX_COMMITS:] if total > MAX_COMMITS else commits
    author_lbl = _author_label(lang)
    for c in shown:
        sha = c.get("sha", "")[:7]
        url = c.get("html_url", "")
        msg = _short_msg((c.get("commit") or {}).get("message", ""))
        author = (c.get("commit") or {}).get("author") or {}
        author_name = author.get("name") or "?"
        date = _fmt_iso(author.get("date"))
        lines.append(
            f'• <a href="{esc(url)}"><code>{esc(sha)}</code></a> — {esc(msg)}\n'
            f"  👤 {esc(author_name)}  {e(DUCK_WATCH)} {date}"
        )

    if total > MAX_COMMITS:
        lines.append("  " + t("report_more", lang, count=total - MAX_COMMITS))

    if files:
        lines.append("")
        lines.append(t("report_changed_files", lang, count=len(files)))
        for f in files[:MAX_FILES]:
            status = f.get("status", "")
            icon = STATUS_ICONS.get(status, "⚪")
            filename = esc(f.get("filename", ""))
            adds = f.get("additions", 0)
            dels = f.get("deletions", 0)
            lines.append(f"  {icon} <code>{filename}</code>  <i>+{adds} -{dels}</i>")
        if len(files) > MAX_FILES:
            lines.append("  " + t("report_more", lang, count=len(files) - MAX_FILES))

    return "\n".join(lines)


def format_single_commit(owner: str, repo: str, commit_detail: dict, lang: str = "ru") -> str:
    """Fallback для одного коммита (когда compare не сработал)."""
    sha = commit_detail.get("sha", "")[:7]
    url = commit_detail.get("html_url", "")
    msg = _short_msg((commit_detail.get("commit") or {}).get("message", ""))
    author = (commit_detail.get("commit") or {}).get("author") or {}
    author_name = author.get("name") or "?"
    date = _fmt_iso(author.get("date"))
    files = commit_detail.get("files") or []

    lines = []
    lines.append(t("report_repo_update", lang, bell=e(DUCK_BELL)))
    lines.append(
        f'{e(DUCK_LAPTOP)} <a href="https://github.com/{esc(owner)}/{esc(repo)}">{esc(owner)}/{esc(repo)}</a>'
    )
    lines.append("")
    lines.append(
        f'• <a href="{esc(url)}"><code>{esc(sha)}</code></a> — {esc(msg)}\n'
        f"  👤 {esc(author_name)}  {e(DUCK_WATCH)} {date}"
    )

    if files:
        lines.append("")
        lines.append(t("report_changed_files", lang, count=len(files)))
        for f in files[:MAX_FILES]:
            status = f.get("status", "")
            icon = STATUS_ICONS.get(status, "⚪")
            filename = esc(f.get("filename", ""))
            adds = f.get("additions", 0)
            dels = f.get("deletions", 0)
            lines.append(f"  {icon} <code>{filename}</code>  <i>+{adds} -{dels}</i>")
        if len(files) > MAX_FILES:
            lines.append("  " + t("report_more", lang, count=len(files) - MAX_FILES))

    return "\n".join(lines)


# --- События пользователей/организаций ---------------------------------

def _event_repo_url(ev: dict) -> str:
    repo = ev.get("repo") or {}
    name = repo.get("name") or ""
    return f"https://github.com/{name}"


def _format_event_line(ev: dict, lang: str) -> Optional[str]:
    """Отрендерить одно событие. None — событие пропустить."""
    etype = ev.get("type")
    payload = ev.get("payload") or {}
    repo = ev.get("repo") or {}
    repo_name = esc(repo.get("name") or "")
    repo_url = esc(_event_repo_url(ev))
    date = _fmt_iso(ev.get("created_at"))

    head = None
    body = None

    if etype == "PushEvent":
        commits = payload.get("commits") or []
        ref = esc((payload.get("ref") or "").replace("refs/heads/", "") or "?")
        head = f"{e(DUCK_LAPTOP)} <b>PushEvent</b> — <a href=\"{repo_url}\">{repo_name}</a>"
        body = t("event_push_body", lang, count=len(commits), branch=ref)

    elif etype == "CreateEvent":
        ref_type = payload.get("ref_type") or ""
        ref = esc(payload.get("ref") or "")
        head = f"{e(DUCK_CHECK)} <b>CreateEvent</b> — <a href=\"{repo_url}\">{repo_name}</a>"
        if ref_type == "repository":
            body = t("event_create_repository", lang)
        elif ref_type == "branch":
            body = t("event_create_branch", lang, ref=ref)
        elif ref_type == "tag":
            body = t("event_create_tag", lang, ref=ref)
        else:
            body = t("event_create_other", lang, ref_type=esc(ref_type), ref=ref)

    elif etype == "ForkEvent":
        forkee = esc((payload.get("forkee") or {}).get("full_name") or "?")
        head = f"🍴 <b>ForkEvent</b> — <a href=\"{repo_url}\">{repo_name}</a>"
        body = t("event_fork_body", lang, forkee=forkee)

    elif etype == "WatchEvent":
        head = f"⭐ <b>WatchEvent</b> — <a href=\"{repo_url}\">{repo_name}</a>"
        body = t("event_watch_body", lang)

    elif etype == "ReleaseEvent":
        rel = payload.get("release") or {}
        tag = esc(rel.get("tag_name") or "?")
        name = rel.get("name") or ""
        head = f"🚀 <b>ReleaseEvent</b> — <a href=\"{repo_url}\">{repo_name}</a>"
        if name and name != (rel.get("tag_name") or ""):
            body = t("event_release_body_named", lang, tag=tag, name=esc(name))
        else:
            body = t("event_release_body", lang, tag=tag)

    elif etype == "IssuesEvent":
        action = (payload.get("action") or "").capitalize()
        title = esc((payload.get("issue") or {}).get("title") or "")
        head = f"📌 <b>IssuesEvent</b> — <a href=\"{repo_url}\">{repo_name}</a>"
        body = t("event_issues_body", lang, action=esc(action), title=title)

    elif etype == "PullRequestEvent":
        action = payload.get("action") or ""
        pr = payload.get("pull_request") or {}
        title = esc(pr.get("title") or "")
        merged = pr.get("merged")
        if action == "closed" and merged:
            action_label = t("event_pr_merged", lang)
        else:
            action_label = action.capitalize()
        head = f"🔀 <b>PullRequestEvent</b> — <a href=\"{repo_url}\">{repo_name}</a>"
        body = t("event_pr_body", lang, action=esc(action_label), title=title)

    elif etype == "PublicEvent":
        head = f"📢 <b>PublicEvent</b> — <a href=\"{repo_url}\">{repo_name}</a>"
        body = t("event_public_body", lang)

    else:
        return None

    return f"• {head}\n  {body}\n  {e(DUCK_WATCH)} {date}"


def format_user_events_report(login: str, events: list[dict], lang: str = "ru") -> Optional[str]:
    rendered = []
    for ev in events:
        line = _format_event_line(ev, lang)
        if line:
            rendered.append(line)
        if len(rendered) >= MAX_EVENTS:
            break
    if not rendered:
        return None

    head = t("report_user_activity", lang, person=e(DUCK_PERSON), login=esc(login)) + "\n"
    return head + "\n" + "\n\n".join(rendered)


def format_org_events_report(org_login: str, events: list[dict], lang: str = "ru") -> Optional[str]:
    rendered = []
    for ev in events:
        line = _format_event_line(ev, lang)
        if line:
            rendered.append(line)
        if len(rendered) >= MAX_EVENTS:
            break
    if not rendered:
        return None

    head = t("report_org_activity", lang, building=e(DUCK_BUILDING), login=esc(org_login)) + "\n"
    return head + "\n" + "\n\n".join(rendered)
