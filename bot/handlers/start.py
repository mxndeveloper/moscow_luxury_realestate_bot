""" from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, _: dict):
    await message.answer("👋 Welcome! Use /language to choose your language.") """

...

from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Bot is alive (direct)!")