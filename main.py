import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Update

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Configuration ----------
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

DOMAIN = os.getenv("DOMAIN")
if not DOMAIN:
    raise ValueError("DOMAIN environment variable missing")

WEBHOOK_URL = f"https://{DOMAIN}/webhook"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- Bot handlers ----------
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Bot is alive!")

# ---------- FastAPI lifespan (startup / shutdown) ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: set webhook
    logger.info("Deleting old webhook...")
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info(f"Setting webhook to {WEBHOOK_URL}")
    await bot.set_webhook(url=WEBHOOK_URL)
    logger.info("Webhook set successfully")
    yield
    # Shutdown: clean up
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

# ---------- HTTP endpoints ----------
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is healthy"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Internal error")