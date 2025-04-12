
from flask import Flask
import os
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    print(f"Telegram response: {response.text}")
    return response

@app.route("/")
def index():
    return "Sniper bot is online 🟢"

@app.route("/fire")
def fire():
    send_telegram_message("🔥 TEST ALERT: Sniper Bot Connected & Active!")
    return "Message sent!"

app.run(host="0.0.0.0", port=5000)
