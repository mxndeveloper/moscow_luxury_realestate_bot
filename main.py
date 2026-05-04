import os
from fastapi import FastAPI, Request
from aiogram import Bot, types
from aiogram.types import Update
from contextlib import asynccontextmanager

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOMAIN = os.getenv("DOMAIN")
WEBHOOK_URL = f"https://{DOMAIN}/webhook"

bot = Bot(token=BOT_TOKEN)
app = FastAPI()

@asynccontextmanager
async def lifespan(app):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")
    yield
    await bot.session.close()
app.router.lifespan_context = lifespan

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    if update.message and update.message.text == "/start":
        await bot.send_message(update.message.chat.id, "Bot is alive (webhook)!")
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}