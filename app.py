from flask import Flask, request
import os
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
BOT_ALIAS = os.getenv("BOT_ALIAS", "Sniper Bot")

@app.route("/")
def home():
    return "Sniper Bot is active!"

@app.route("/signal", methods=["POST"])
def send_telegram_message():
    data = request.get_json()
    coin_name = data.get("coin", "Unknown")
    roi = data.get("roi", "N/A")
    entry_price = data.get("entry", "N/A")

    message = f"🚨 {BOT_ALIAS} ALERT 🚨\nCoin: {coin_name}\nROI: {roi}\nEntry: {entry_price}"
    send_to_telegram(message)
    return {"status": "ok"}

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
