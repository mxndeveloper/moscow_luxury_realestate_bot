# Moscow Real Estate Bot

Telegram bot with webhook architecture, ready to deploy on bothost.ru.

## Local testing

1. Create `.env` from `.env.example` and fill in `BOT_TOKEN`.
2. Run `ngrok http 8000` and set `WEBHOOK_URL` in `.env` to the ngrok HTTPS URL.
3. Install dependencies: `pip install -r requirements.txt`
4. Run `python main.py`

## Deploy to bothost

Push to GitHub, connect repo in bothost dashboard, and deploy.
