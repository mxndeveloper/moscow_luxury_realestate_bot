import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Update

# ---------- Configuration ----------
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

DOMAIN = os.getenv("DOMAIN")            # e.g., "bot-1234.bothost.tech"
WEBHOOK_URL = f"https://{DOMAIN}/webhook" if DOMAIN else None

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Bot is alive!")

# ---------- Webhook Mode (if DOMAIN is set) ----------
if DOMAIN:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Delete old webhook and set the new one
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Webhook set to {WEBHOOK_URL}")
        yield
        await bot.session.close()

    app = FastAPI(lifespan=lifespan)

    @app.post("/webhook")
    async def telegram_webhook(request: Request):
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}

    @app.get("/")
    async def health():
        return {"status": "ok", "message": "Bot is running"}

    # For local testing with uvicorn, you can run:
    # if __name__ == "__main__":
    #     import uvicorn
    #     uvicorn.run("main:app", host="0.0.0.0", port=8000)
    # On Bothost, the platform runs uvicorn automatically.

# ---------- Polling Mode Fallback (if DOMAIN is missing) ----------
else:
    async def polling_main():
        await bot.delete_webhook(drop_pending_updates=True)
        print("🔄 Polling mode started")
        await dp.start_polling(bot)

    if __name__ == "__main__":
        asyncio.run(polling_main())