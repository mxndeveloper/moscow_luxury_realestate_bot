from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards import get_language_keyboard   # note: we will add this later, but for now comment it out

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, _: dict):
    await message.answer("👋 Welcome! Minimal start handler works.")