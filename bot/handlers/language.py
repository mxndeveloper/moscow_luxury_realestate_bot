from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from keyboards import get_language_keyboard, get_role_keyboard

router = Router()
user_lang = {}
user_role = {}

@router.message(Command("language"))
async def change_language(message: types.Message):
    await message.answer("🌐 Choose language / Выберите язык", reply_markup=get_language_keyboard())

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_lang[callback.from_user.id] = lang
    await callback.answer(f"Language set to {'English' if lang == 'en' else 'Русский'}")
    await callback.message.answer("✅ Language saved! Now choose your role:", reply_markup=get_role_keyboard())

@router.callback_query(F.data.startswith("role_"))
async def set_role(callback: CallbackQuery):
    role = "realtor" if callback.data == "role_realtor" else "client"
    user_role[callback.from_user.id] = role
    await callback.answer()
    await callback.message.answer(f"✅ Role set to {'Realtor' if role == 'realtor' else 'Client'}! Use /menu to start.")