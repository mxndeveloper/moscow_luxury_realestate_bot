import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from contextlib import asynccontextmanager

# Import your routers and middleware
from bot.handlers.start import router as start_router
from bot.handlers.language import router as language_router
from bot.handlers.menu import router as menu_router
from bot.middlewares.i18n import I18nMiddleware

# ---------- Configuration ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
DOMAIN = os.getenv("DOMAIN")
if not BOT_TOKEN or not DOMAIN:
    raise ValueError("Missing BOT_TOKEN or DOMAIN")

WEBHOOK_URL = f"https://{DOMAIN}/webhook"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- Middleware & Routers ----------
dp.update.middleware(I18nMiddleware())
dp.include_router(start_router)
dp.include_router(language_router)
dp.include_router(menu_router)

# ---------- Webhook Lifespan ----------
@asynccontextmanager
async def lifespan(app):
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook set to {WEBHOOK_URL}")
    except Exception as e:
        print(f"❌ Webhook set failed: {e}")
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

# ---------- Endpoints ----------
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/health")
async def health_check():
    return {"status": "ok"}