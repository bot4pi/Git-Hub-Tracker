from aiogram import Router

from . import start, repos, users, orgs, watchlist, language


def setup_routers() -> Router:
    root = Router(name="root")
    root.include_router(start.router)
    root.include_router(repos.router)
    root.include_router(users.router)
    root.include_router(orgs.router)
    root.include_router(watchlist.router)
    root.include_router(language.router)
    return root
