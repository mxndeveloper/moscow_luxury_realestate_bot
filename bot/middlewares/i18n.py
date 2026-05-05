import json
from aiogram import BaseMiddleware

class I18nMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        with open("locales/ru.json", "r", encoding="utf-8") as f:
            translations = json.load(f)
        data["_"] = translations
        return await handler(event, data)