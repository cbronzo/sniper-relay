# Sniper Relay Bot

This Flask app listens for sniper alert signals and sends messages to a Telegram channel.

## Setup

1. Set your environment variables in your Railway project:
   - TELEGRAM_BOT_TOKEN
   - TELEGRAM_CHANNEL_ID
   - BOT_ALIAS (ex: "Sniper Elite")
   - SNIPER_SECRET (ex: "moonaccess123")
2. Deploy the app on Railway.
3. To trigger an alert, send a POST request to the /signal endpoint with a JSON payload.
