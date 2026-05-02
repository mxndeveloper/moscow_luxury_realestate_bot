from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("menu"))
async def menu(message: types.Message, _: dict):
    await message.answer(
        "🏠 *Главное меню / Main Menu*\n\n"
        "• /search – Найти недвижимость\n"
        "• /list – Мои объявления\n"
        "• /language – Сменить язык\n"
        "• /help – Помощь",
        parse_mode="Markdown"
    )