# import logging
# from contextlib import asynccontextmanager
# from fastapi import FastAPI, Request, HTTPException
# from aiogram import Bot, Dispatcher
# from aiogram.types import Update

# from bot.config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_SECRET
# from bot.handlers import register_handlers

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
# register_handlers(dp)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("Starting bot...")
#     await bot.delete_webhook(drop_pending_updates=True)
#     await bot.set_webhook(
#         url=WEBHOOK_URL,
#         secret_token=WEBHOOK_SECRET or None,
#         drop_pending_updates=True
#     )
#     logger.info(f"Webhook set to {WEBHOOK_URL}")
#     yield
#     await bot.session.close()

# app = FastAPI(lifespan=lifespan)

# @app.post("/webhook")
# async def telegram_webhook(request: Request):
#     if WEBHOOK_SECRET:
#         secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
#         if secret != WEBHOOK_SECRET:
#             raise HTTPException(status_code=403, detail="Forbidden")
#     try:
#         data = await request.json()
#         update = Update.model_validate(data)
#         await dp.feed_update(bot, update)
#         return {"ok": True}
#     except Exception as e:
#         logger.error(f"Error: {e}")
#         return {"ok": False}
    
# # Add this at the end of main.py
# async def main():
#     if WEBHOOK_URL and "localhost" not in WEBHOOK_URL and "ngrok" not in WEBHOOK_URL:
#         # Production: run webhook mode
#         import uvicorn
#         uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
#     else:
#         # Local development: use polling
#         print("🌱 Running in polling mode for local testing")
#         await bot.delete_webhook(drop_pending_updates=True)
#         await dp.start_polling(bot)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())


# ...

import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Load .env only if it exists (safe for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed – assume env vars are set directly

# Get token from environment (Bothost injects it, or set locally in .env)
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set – please provide token in environment or .env file")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Bot is alive!")

async def main():
    print("🤖 Bot started. Waiting for messages...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())