""" import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from bot.handlers.start import router as start_router
from bot.handlers.language import router as language_router
from bot.handlers.menu import router as menu_router
from bot.middlewares.i18n import I18nMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

DOMAIN = os.getenv("DOMAIN")
if not DOMAIN:
    raise ValueError("DOMAIN environment variable missing")

WEBHOOK_URL = f"https://{DOMAIN}/webhook"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.update.middleware(I18nMiddleware())
dp.include_router(start_router)
dp.include_router(language_router)
dp.include_router(menu_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Deleting old webhook...")
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info(f"Setting webhook to {WEBHOOK_URL}")
    await bot.set_webhook(url=WEBHOOK_URL)
    logger.info("Webhook set")
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

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
     """

    ####

import os
from fastapi import FastAPI, Request
from aiogram import Bot, types
from aiogram.types import Update

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOMAIN = os.getenv("DOMAIN")
WEBHOOK_URL = f"https://{DOMAIN}/webhook"

bot = Bot(token=BOT_TOKEN)
app = FastAPI()

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

from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")
    yield
    await bot.session.close()
app.router.lifespan_context = lifespan