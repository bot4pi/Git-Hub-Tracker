import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))
DB_PATH = os.getenv("DB_PATH", "tracker.db").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")
