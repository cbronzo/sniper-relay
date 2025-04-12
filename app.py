from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")

@app.route("/")
def home():
    return "Sniper Relay is active!"

@app.route("/signal", methods=["POST"])
def sniper_signal():
    try:
        data = request.json
        coin = data.get("coin")
        roi = data.get("roi")
        entry = data.get("entry")
        note = data.get("note", "")

        if not coin or not roi or not entry:
            return jsonify({"error": "Missing required fields"}), 400

        message = (
            f"🚨 SNIPER ALERT\n\n"
            f"🪙 Coin: {coin}\n"
            f"💰 Entry: {entry}\n"
            f"📈 Target ROI: {roi}\n"
            f"📝 {note}"
        )

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": message
        }

        response = requests.post(telegram_url, json=payload)
        print(f"Telegram API Response: {response.status_code} - {response.text}")

        return jsonify({"status": "sent", "message": message})

    except Exception as e:
        print(f"Error in /signal: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
