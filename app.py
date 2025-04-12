from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Telegram setup
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

@app.route("/")
def home():
    return "Sniper relay is active."

@app.route("/signal", methods=["POST"])
def sniper_signal():
    try:
        data = request.json
        coin = data.get("coin")
        score = data.get("score")
        price = data.get("price")
        note = data.get("note", "")

        if not coin or not score:
            return jsonify({"error": "Missing data"}), 400

        message = f"🚨 Sniper Alert\n\n🪙 Coin: {coin}\n📈 Score: {score}\n💵 Price: {price}\n📝 {note}"

        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": message
        }
        response = requests.post(telegram_url, json=payload)
        return jsonify({"status": "sent", "telegram_response": response.json()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
