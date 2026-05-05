import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers.start import router as start_router
from bot.handlers.language import router as language_router
from bot.handlers.menu import router as menu_router
from bot.middlewares.i18n import I18nMiddleware

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.update.middleware(I18nMiddleware())
dp.include_router(start_router)
dp.include_router(language_router)
dp.include_router(menu_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("🤖 Bot started (polling mode)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())