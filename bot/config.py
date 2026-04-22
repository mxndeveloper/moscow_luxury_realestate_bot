import os
import logging

logger = logging.getLogger(__name__)

def get_env(key: str, default: str = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value

# Try multiple possible token names (bothost provides BOT_TOKEN, API_TOKEN, etc.)
BOT_TOKEN = (
    os.getenv("BOT_TOKEN") or
    os.getenv("API_TOKEN") or
    os.getenv("TELEGRAM_BOT_TOKEN") or
    os.getenv("TOKEN")
)
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found in environment")

# Webhook URL: either from env, or construct from DOMAIN (bothost), or fallback for local testing
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    domain = os.getenv("DOMAIN")
    if domain:
        WEBHOOK_URL = f"https://{domain}/webhook"
    else:
        WEBHOOK_URL = "http://localhost:8000/webhook"

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

logger.info(f"BOT_TOKEN loaded (first 10 chars): {BOT_TOKEN[:10]}...")
logger.info(f"WEBHOOK_URL = {WEBHOOK_URL}")
