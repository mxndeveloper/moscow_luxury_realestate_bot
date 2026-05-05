from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards import get_language_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, _: dict):
    await message.answer("👋 Добро пожаловать! Выберите язык / Choose language",
                         reply_markup=get_language_keyboard())