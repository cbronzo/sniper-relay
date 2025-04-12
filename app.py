
import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

BOT_ALIAS = os.getenv("BOT_ALIAS", "Sniper Relay")

def send_telegram_message(text):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🚨 {BOT_ALIAS} Alert:\n{text}",
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)

def send_discord_message(text):
    if DISCORD_WEBHOOK_URL:
        payload = {
            "content": f"🚨 **{BOT_ALIAS} Alert**\n{text}"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", "⚠️ No message content")
    send_telegram_message(message)
    send_discord_message(message)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
