import json
from aiogram import BaseMiddleware

class I18nMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            with open("locales/ru.json", "r", encoding="utf-8") as f:
                translations = json.load(f)
        except:
            translations = {}
        data["_"] = translations
        return await handler(event, data)