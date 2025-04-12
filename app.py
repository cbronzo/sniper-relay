from flask import Flask
import requests
import os

app = Flask(__name__)

# Load environment variables
BOT_ALIAS = os.environ.get("BOT_ALIAS", "Sniper")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")

def send_telegram_message(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        print("❌ Bot token or channel ID missing.")
        return

    print(f"📤 Sending message to Telegram...\nChannel ID: {TELEGRAM_CHANNEL_ID}\nMessage: {text}")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": f"{BOT_ALIAS}: {text}"
    }

    try:
        response = requests.post(url, json=payload)
        print(f"✅ Telegram API Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception while sending Telegram message: {e}")

@app.route("/")
def home():
    print("🌐 / endpoint hit. Running send_telegram_message test.")
    send_telegram_message("🔥 Connected and working! This is your Sniper bot test.")
    return "Sniper Relay Bot is active!"

# Ensure the app runs on Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway injects PORT
    app.run(host="0.0.0.0", port=port)
