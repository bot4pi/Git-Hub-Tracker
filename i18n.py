"""
Простой i18n: словари строк для ru/en + функция t().

Все строки могут содержать HTML-разметку (Telegram parse_mode=HTML).
Подстановки делаются через str.format(**kwargs). Любые пользовательские
данные ОБЯЗАНЫ быть HTML-экранированы ДО передачи в t().
"""

from typing import Optional

DEFAULT_LANG = "ru"
SUPPORTED_LANGS = ("ru", "en")


def lang_for_user(stored_lang: Optional[str], telegram_lang_code: Optional[str]) -> str:
    """
    Выбрать язык:
      1. Сохранённый в БД, если валидный
      2. Иначе из Telegram language_code: en → en, всё остальное → ru
    """
    if stored_lang in SUPPORTED_LANGS:
        return stored_lang
    code = (telegram_lang_code or "").lower()
    if code.startswith("en"):
        return "en"
    return DEFAULT_LANG


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    """Вернуть переведённую строку по ключу с подстановкой kwargs."""
    table = TRANSLATIONS.get(lang) or TRANSLATIONS[DEFAULT_LANG]
    template = table.get(key)
    if template is None:
        template = TRANSLATIONS[DEFAULT_LANG].get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template
    return template


TRANSLATIONS: dict[str, dict[str, str]] = {
    "ru": {
        # /start, /help
        "welcome": (
            "{wave} <b>Привет! Я слежу за GitHub для тебя.</b>\n\n"
            "Что я умею:\n"
            "{laptop} Отслеживать репозитории — новые коммиты\n"
            "{person} Следить за пользователями — их активность\n"
            "{building} Мониторить организации — публичные события\n\n"
            "<b>Команды:</b>\n"
            "• <code>/addrepo &lt;url&gt;</code> — добавить репозиторий\n"
            "• <code>/adduser &lt;login&gt;</code> — добавить пользователя\n"
            "• <code>/addorg &lt;login&gt;</code> — добавить организацию\n"
            "• <code>/list</code> — твой список\n"
            "• <code>/removerepo</code> / <code>/removeuser</code> / <code>/removeorg</code> — удалить\n"
            "• <code>/language</code> — сменить язык"
        ),
        "add_hint": (
            "{plus} <b>Добавить новый объект</b>\n\n"
            "{laptop} <code>/addrepo https://github.com/owner/repo</code>\n"
            "{person} <code>/adduser login</code>\n"
            "{building} <code>/addorg login</code>"
        ),
        "menu_repos_text": (
            "{laptop} <b>Репозитории</b>\n\n"
            "• <code>/addrepo &lt;url&gt;</code> — добавить\n"
            "• <code>/removerepo &lt;owner/repo&gt;</code> — удалить\n"
            "• <code>/list</code> — список"
        ),
        "menu_users_text": (
            "{person} <b>Пользователи GitHub</b>\n\n"
            "• <code>/adduser &lt;login&gt;</code> — добавить\n"
            "• <code>/removeuser &lt;login&gt;</code> — удалить\n"
            "• <code>/list</code> — список"
        ),
        "menu_orgs_text": (
            "{building} <b>Организации</b>\n\n"
            "• <code>/addorg &lt;login&gt;</code> — добавить\n"
            "• <code>/removeorg &lt;login&gt;</code> — удалить\n"
            "• <code>/list</code> — список"
        ),
        "menu_add_repo_text": (
            "{laptop} <b>Добавить репозиторий</b>\n\n"
            "Используй: <code>/addrepo https://github.com/owner/repo</code>"
        ),
        "menu_add_user_text": (
            "{person} <b>Добавить пользователя GitHub</b>\n\n"
            "Используй: <code>/adduser octocat</code>"
        ),
        "menu_add_org_text": (
            "{building} <b>Добавить организацию</b>\n\n"
            "Используй: <code>/addorg github</code>"
        ),

        # Кнопки
        "btn_repos":     "Репо",
        "btn_users":     "Юзеры",
        "btn_orgs":      "Орги",
        "btn_list":      "Мой список",
        "btn_add_more":  "Добавить ещё",
        "btn_add_repo":  "+ Репо",
        "btn_add_user":  "+ Юзер",
        "btn_add_org":   "+ Орг",
        "btn_lang_ru":   "Русский",
        "btn_lang_en":   "English",

        # /addrepo
        "addrepo_bad_format": (
            "{search} <b>Неверный формат.</b>\n\n"
            "Пример: <code>/addrepo https://github.com/owner/repo</code>"
        ),
        "addrepo_not_found": (
            "{search} <b>Репозиторий не найден на GitHub.</b>\n\n"
            "<code>{owner}/{repo}</code>"
        ),
        "addrepo_already": (
            "{laptop} <b>Уже отслеживается.</b>\n\n"
            '<a href="{url}">{owner}/{repo}</a>'
        ),
        "addrepo_added": (
            "{check} <b>Репозиторий добавлен.</b>\n\n"
            '{laptop} <a href="{url}">{owner}/{repo}</a>\n\n'
            "<i>Уведомления придут при следующих коммитах.</i>"
        ),

        # /removerepo
        "removerepo_specify": (
            "{trash} <b>Укажи репозиторий.</b>\n\n"
            "Пример: <code>/removerepo owner/repo</code>"
        ),
        "removerepo_bad_format": (
            "{trash} <b>Неверный формат.</b>\n\n"
            "Пример: <code>/removerepo owner/repo</code>"
        ),
        "removerepo_not_in_list": (
            "{search} <b>Не найдено в твоём списке.</b>\n\n"
            "<code>{owner}/{repo}</code>"
        ),
        "removerepo_removed": (
            "{trash} <b>Репозиторий удалён.</b>\n\n"
            "<code>{owner}/{repo}</code>"
        ),

        # /adduser
        "adduser_bad_format": (
            "{search} <b>Неверный формат.</b>\n\n"
            "Пример: <code>/adduser octocat</code>"
        ),
        "adduser_not_found": (
            "{search} <b>Пользователь не найден.</b>\n\n"
            "<code>{login}</code>\n\n"
            "<i>Если это организация — используй /addorg.</i>"
        ),
        "adduser_already": (
            "{person} <b>Уже отслеживается.</b>\n\n"
            '<a href="https://github.com/{login}">{login}</a>'
        ),
        "adduser_added": (
            "{check} <b>Пользователь добавлен.</b>\n\n"
            '{person} <a href="https://github.com/{login}">{login}</a>\n\n'
            "<i>Уведомления придут при новой активности.</i>"
        ),

        # /removeuser
        "removeuser_specify": (
            "{trash} <b>Укажи логин.</b>\n\n"
            "Пример: <code>/removeuser octocat</code>"
        ),
        "removeuser_not_in_list": (
            "{search} <b>Не найдено в твоём списке.</b>\n\n"
            "<code>{login}</code>"
        ),
        "removeuser_removed": (
            "{trash} <b>Пользователь удалён.</b>\n\n"
            "<code>{login}</code>"
        ),

        # /addorg
        "addorg_bad_format": (
            "{search} <b>Неверный формат.</b>\n\n"
            "Пример: <code>/addorg github</code>"
        ),
        "addorg_not_found": (
            "{search} <b>Организация не найдена.</b>\n\n"
            "<code>{login}</code>\n\n"
            "<i>Если это пользователь — используй /adduser.</i>"
        ),
        "addorg_already": (
            "{building} <b>Уже отслеживается.</b>\n\n"
            '<a href="https://github.com/{login}">{login}</a>'
        ),
        "addorg_added": (
            "{check} <b>Организация добавлена.</b>\n\n"
            '{building} <a href="https://github.com/{login}">{login}</a>\n\n'
            "<i>Уведомления придут при новых событиях.</i>"
        ),

        # /removeorg
        "removeorg_specify": (
            "{trash} <b>Укажи логин.</b>\n\n"
            "Пример: <code>/removeorg github</code>"
        ),
        "removeorg_not_in_list": (
            "{search} <b>Не найдено в твоём списке.</b>\n\n"
            "<code>{login}</code>"
        ),
        "removeorg_removed": (
            "{trash} <b>Организация удалена.</b>\n\n"
            "<code>{login}</code>"
        ),

        # /list
        "list_title":          "{list} <b>Твой список мониторинга</b>",
        "list_section_repos":  "{laptop} <b>Репозитории ({count}):</b>",
        "list_section_users":  "{person} <b>Пользователи ({count}):</b>",
        "list_section_orgs":   "{building} <b>Организации ({count}):</b>",
        "list_next_check":     "{watch} Следующая проверка через ~{minutes} мин.",
        "list_empty": (
            "{search} <b>Ты ещё ничего не отслеживаешь.</b>\n\n"
            "Добавь первый объект:\n"
            "• <code>/addrepo &lt;url&gt;</code>\n"
            "• <code>/adduser &lt;login&gt;</code>\n"
            "• <code>/addorg &lt;login&gt;</code>"
        ),

        # /language
        "language_choose": (
            "🌐 <b>Выбери язык</b>\n\n"
            "Choose your language."
        ),
        "language_set_ru": "{check} Язык переключён на <b>русский</b>.",
        "language_set_en": "{check} Language set to <b>English</b>.",

        # Отчёты (формат)
        "report_repo_update":  "{bell} <b>Обновление репозитория</b>",
        "report_new_commits":  "{fire} <b>Новых коммитов: {count}</b>",
        "report_more":         "<i>… и ещё {count}</i>",
        "report_changed_files":"📁 <b>Изменённые файлы ({count}):</b>",
        "report_user_activity":(
            "{person} <b>Активность пользователя</b>\n"
            '👤 <a href="https://github.com/{login}">{login}</a>'
        ),
        "report_org_activity": (
            "{building} <b>Активность организации</b>\n"
            '🏢 <a href="https://github.com/{login}">{login}</a>'
        ),

        # События
        "event_push_body":          "Запушил {count} коммит(ов) в ветку <code>{branch}</code>",
        "event_create_repository":  "Создал новый репозиторий",
        "event_create_branch":      "Создал ветку <code>{ref}</code>",
        "event_create_tag":         "Создал тег <code>{ref}</code>",
        "event_create_other":       "Создал {ref_type} <code>{ref}</code>",
        "event_fork_body":          "Форкнул в <code>{forkee}</code>",
        "event_watch_body":         "Поставил звезду",
        "event_release_body":       "Новый релиз <code>{tag}</code>",
        "event_release_body_named": "Новый релиз <code>{tag}</code> — {name}",
        "event_issues_body":        "{action} issue: {title}",
        "event_pr_body":            "{action} PR: {title}",
        "event_pr_merged":          "Merged",
        "event_public_body":        "Репозиторий стал публичным",

        # Команды бота (для set_my_commands)
        "cmd_start":      "Запустить бота",
        "cmd_help":       "Помощь",
        "cmd_list":       "Мой список мониторинга",
        "cmd_addrepo":    "Добавить репозиторий",
        "cmd_removerepo": "Удалить репозиторий",
        "cmd_adduser":    "Добавить пользователя GitHub",
        "cmd_removeuser": "Удалить пользователя",
        "cmd_addorg":     "Добавить организацию",
        "cmd_removeorg":  "Удалить организацию",
        "cmd_language":   "Сменить язык",
    },

    "en": {
        "welcome": (
            "{wave} <b>Hi! I track GitHub for you.</b>\n\n"
            "What I can do:\n"
            "{laptop} Watch repositories — new commits\n"
            "{person} Follow users — their activity\n"
            "{building} Monitor organizations — public events\n\n"
            "<b>Commands:</b>\n"
            "• <code>/addrepo &lt;url&gt;</code> — add a repository\n"
            "• <code>/adduser &lt;login&gt;</code> — add a user\n"
            "• <code>/addorg &lt;login&gt;</code> — add an organization\n"
            "• <code>/list</code> — your watch list\n"
            "• <code>/removerepo</code> / <code>/removeuser</code> / <code>/removeorg</code> — remove\n"
            "• <code>/language</code> — change language"
        ),
        "add_hint": (
            "{plus} <b>Add a new target</b>\n\n"
            "{laptop} <code>/addrepo https://github.com/owner/repo</code>\n"
            "{person} <code>/adduser login</code>\n"
            "{building} <code>/addorg login</code>"
        ),
        "menu_repos_text": (
            "{laptop} <b>Repositories</b>\n\n"
            "• <code>/addrepo &lt;url&gt;</code> — add\n"
            "• <code>/removerepo &lt;owner/repo&gt;</code> — remove\n"
            "• <code>/list</code> — list"
        ),
        "menu_users_text": (
            "{person} <b>GitHub users</b>\n\n"
            "• <code>/adduser &lt;login&gt;</code> — add\n"
            "• <code>/removeuser &lt;login&gt;</code> — remove\n"
            "• <code>/list</code> — list"
        ),
        "menu_orgs_text": (
            "{building} <b>Organizations</b>\n\n"
            "• <code>/addorg &lt;login&gt;</code> — add\n"
            "• <code>/removeorg &lt;login&gt;</code> — remove\n"
            "• <code>/list</code> — list"
        ),
        "menu_add_repo_text": (
            "{laptop} <b>Add a repository</b>\n\n"
            "Use: <code>/addrepo https://github.com/owner/repo</code>"
        ),
        "menu_add_user_text": (
            "{person} <b>Add a GitHub user</b>\n\n"
            "Use: <code>/adduser octocat</code>"
        ),
        "menu_add_org_text": (
            "{building} <b>Add an organization</b>\n\n"
            "Use: <code>/addorg github</code>"
        ),

        "btn_repos":     "Repos",
        "btn_users":     "Users",
        "btn_orgs":      "Orgs",
        "btn_list":      "My list",
        "btn_add_more":  "Add more",
        "btn_add_repo":  "+ Repo",
        "btn_add_user":  "+ User",
        "btn_add_org":   "+ Org",
        "btn_lang_ru":   "Русский",
        "btn_lang_en":   "English",

        "addrepo_bad_format": (
            "{search} <b>Invalid format.</b>\n\n"
            "Example: <code>/addrepo https://github.com/owner/repo</code>"
        ),
        "addrepo_not_found": (
            "{search} <b>Repository not found on GitHub.</b>\n\n"
            "<code>{owner}/{repo}</code>"
        ),
        "addrepo_already": (
            "{laptop} <b>Already tracked.</b>\n\n"
            '<a href="{url}">{owner}/{repo}</a>'
        ),
        "addrepo_added": (
            "{check} <b>Repository added.</b>\n\n"
            '{laptop} <a href="{url}">{owner}/{repo}</a>\n\n'
            "<i>You will be notified about new commits.</i>"
        ),

        "removerepo_specify": (
            "{trash} <b>Specify a repository.</b>\n\n"
            "Example: <code>/removerepo owner/repo</code>"
        ),
        "removerepo_bad_format": (
            "{trash} <b>Invalid format.</b>\n\n"
            "Example: <code>/removerepo owner/repo</code>"
        ),
        "removerepo_not_in_list": (
            "{search} <b>Not in your list.</b>\n\n"
            "<code>{owner}/{repo}</code>"
        ),
        "removerepo_removed": (
            "{trash} <b>Repository removed.</b>\n\n"
            "<code>{owner}/{repo}</code>"
        ),

        "adduser_bad_format": (
            "{search} <b>Invalid format.</b>\n\n"
            "Example: <code>/adduser octocat</code>"
        ),
        "adduser_not_found": (
            "{search} <b>User not found.</b>\n\n"
            "<code>{login}</code>\n\n"
            "<i>If it is an organization — use /addorg.</i>"
        ),
        "adduser_already": (
            "{person} <b>Already tracked.</b>\n\n"
            '<a href="https://github.com/{login}">{login}</a>'
        ),
        "adduser_added": (
            "{check} <b>User added.</b>\n\n"
            '{person} <a href="https://github.com/{login}">{login}</a>\n\n'
            "<i>You will be notified about new activity.</i>"
        ),

        "removeuser_specify": (
            "{trash} <b>Specify a login.</b>\n\n"
            "Example: <code>/removeuser octocat</code>"
        ),
        "removeuser_not_in_list": (
            "{search} <b>Not in your list.</b>\n\n"
            "<code>{login}</code>"
        ),
        "removeuser_removed": (
            "{trash} <b>User removed.</b>\n\n"
            "<code>{login}</code>"
        ),

        "addorg_bad_format": (
            "{search} <b>Invalid format.</b>\n\n"
            "Example: <code>/addorg github</code>"
        ),
        "addorg_not_found": (
            "{search} <b>Organization not found.</b>\n\n"
            "<code>{login}</code>\n\n"
            "<i>If it is a user — use /adduser.</i>"
        ),
        "addorg_already": (
            "{building} <b>Already tracked.</b>\n\n"
            '<a href="https://github.com/{login}">{login}</a>'
        ),
        "addorg_added": (
            "{check} <b>Organization added.</b>\n\n"
            '{building} <a href="https://github.com/{login}">{login}</a>\n\n'
            "<i>You will be notified about new events.</i>"
        ),

        "removeorg_specify": (
            "{trash} <b>Specify a login.</b>\n\n"
            "Example: <code>/removeorg github</code>"
        ),
        "removeorg_not_in_list": (
            "{search} <b>Not in your list.</b>\n\n"
            "<code>{login}</code>"
        ),
        "removeorg_removed": (
            "{trash} <b>Organization removed.</b>\n\n"
            "<code>{login}</code>"
        ),

        "list_title":          "{list} <b>Your watch list</b>",
        "list_section_repos":  "{laptop} <b>Repositories ({count}):</b>",
        "list_section_users":  "{person} <b>Users ({count}):</b>",
        "list_section_orgs":   "{building} <b>Organizations ({count}):</b>",
        "list_next_check":     "{watch} Next check in ~{minutes} min.",
        "list_empty": (
            "{search} <b>You are not tracking anything yet.</b>\n\n"
            "Add your first target:\n"
            "• <code>/addrepo &lt;url&gt;</code>\n"
            "• <code>/adduser &lt;login&gt;</code>\n"
            "• <code>/addorg &lt;login&gt;</code>"
        ),

        "language_choose": (
            "🌐 <b>Choose your language</b>\n\n"
            "Выбери язык."
        ),
        "language_set_ru": "{check} Язык переключён на <b>русский</b>.",
        "language_set_en": "{check} Language set to <b>English</b>.",

        "report_repo_update":  "{bell} <b>Repository update</b>",
        "report_new_commits":  "{fire} <b>New commits: {count}</b>",
        "report_more":         "<i>… and {count} more</i>",
        "report_changed_files":"📁 <b>Changed files ({count}):</b>",
        "report_user_activity":(
            "{person} <b>User activity</b>\n"
            '👤 <a href="https://github.com/{login}">{login}</a>'
        ),
        "report_org_activity": (
            "{building} <b>Organization activity</b>\n"
            '🏢 <a href="https://github.com/{login}">{login}</a>'
        ),

        "event_push_body":          "Pushed {count} commit(s) to branch <code>{branch}</code>",
        "event_create_repository":  "Created a new repository",
        "event_create_branch":      "Created branch <code>{ref}</code>",
        "event_create_tag":         "Created tag <code>{ref}</code>",
        "event_create_other":       "Created {ref_type} <code>{ref}</code>",
        "event_fork_body":          "Forked to <code>{forkee}</code>",
        "event_watch_body":         "Starred",
        "event_release_body":       "New release <code>{tag}</code>",
        "event_release_body_named": "New release <code>{tag}</code> — {name}",
        "event_issues_body":        "{action} issue: {title}",
        "event_pr_body":            "{action} PR: {title}",
        "event_pr_merged":          "Merged",
        "event_public_body":        "Repository is now public",

        "cmd_start":      "Start the bot",
        "cmd_help":       "Help",
        "cmd_list":       "My watch list",
        "cmd_addrepo":    "Add a repository",
        "cmd_removerepo": "Remove a repository",
        "cmd_adduser":    "Add a GitHub user",
        "cmd_removeuser": "Remove a user",
        "cmd_addorg":     "Add an organization",
        "cmd_removeorg":  "Remove an organization",
        "cmd_language":   "Change language",
    },
}
