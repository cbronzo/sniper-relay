# Sniper Relay Bot

This is a lightweight webhook listener that relays sniper alerts to Telegram and Discord.

## Setup

1. Fill in the `.env` file with your secrets.
2. Deploy using Render, Railway, or Replit.
3. Send a POST request with `{ "message": "Your alert text here" }` to the live URL.
