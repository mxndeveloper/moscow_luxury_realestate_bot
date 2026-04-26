import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Update

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Bot is alive!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Set the webhook
    await bot.delete_webhook(drop_pending_updates=True)
    # --- IMPORTANT: Set your webhook URL here or from config ---
    # await bot.set_webhook(url="https://your-domain.tech/webhook")
    print("✅ Webhook is ready.")
    yield
    # Shutdown: Clean up connections
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

# Production-ready health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is healthy"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}