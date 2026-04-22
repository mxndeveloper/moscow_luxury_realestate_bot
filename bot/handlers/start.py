from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "��� Добро пожаловать в Real Estate Assistant!\n\n"
        "Я тестовый бот. Отправьте /help для списка команд.\n"
        "Примеры запросов:\n"
        "- Студия в Москве до 10 млн\n"
        "- 2‑комнатная квартира в центре"
    )

@router.message()
async def echo_help(message: types.Message):
    await message.answer(
        "Я пока умею только отвечать на /start. "
        "Скоро добавлю поиск недвижимости!"
    )
