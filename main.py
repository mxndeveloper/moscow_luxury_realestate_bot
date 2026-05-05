import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from contextlib import asynccontextmanager
from bot.handlers.start import router as start_router

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOMAIN = os.getenv("DOMAIN")
if not BOT_TOKEN or not DOMAIN:
    raise ValueError("Missing BOT_TOKEN or DOMAIN")

WEBHOOK_URL = f"https://{DOMAIN}/webhook"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(start_router)

app = FastAPI()

@asynccontextmanager
async def lifespan(app):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook set to {WEBHOOK_URL}")
    yield
    await bot.session.close()
app.router.lifespan_context = lifespan

@app.post("/webhook")
async def telegram_webhook(request: Request):
    print("🔵 Webhook called")
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}