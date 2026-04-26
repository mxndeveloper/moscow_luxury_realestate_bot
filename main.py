import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Bot is alive!")

async def main():
    # 🔥 DELETE THE WEBHOOK BEFORE POLLING
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook deleted, starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())