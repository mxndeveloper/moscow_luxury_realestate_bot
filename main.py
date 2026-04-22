import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Update

from bot.config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_SECRET
from bot.handlers import register_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
register_handlers(dp)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET or None,
        drop_pending_updates=True
    )
    logger.info(f"Webhook set to {WEBHOOK_URL}")
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    if WEBHOOK_SECRET:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != WEBHOOK_SECRET:
            raise HTTPException(status_code=403, detail="Forbidden")
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"ok": False}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
