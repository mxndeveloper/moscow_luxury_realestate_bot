import os
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOMAIN = os.getenv("DOMAIN")
if not BOT_TOKEN or not DOMAIN:
    raise ValueError("Missing BOT_TOKEN or DOMAIN")

WEBHOOK_URL = f"https://{DOMAIN}/webhook"
# We don't even need aiogram for this test

app = FastAPI()

@asynccontextmanager
async def lifespan(app):
    import httpx
    async with httpx.AsyncClient() as client:
        await client.post(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook", json={"url": WEBHOOK_URL})
    print(f"✅ Webhook set to {WEBHOOK_URL}")
    yield

app.router.lifespan_context = lifespan

@app.post("/webhook")
async def webhook(request: Request):
    print("🔵 Webhook called")
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}