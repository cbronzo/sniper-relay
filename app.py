from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Load environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
BOT_ALIAS = os.getenv("BOT_ALIAS", "Sniper Bot")
SECRET = os.getenv("SNIPER_SECRET")

@app.route("/")
def home():
    return f"{BOT_ALIAS} is live!"

@app.route("/signal", methods=["POST"])
def sniper_signal():
    try:
        # Authentication check
        key = request.args.get("key")
        if key != SECRET:
            return jsonify({"error": "Unauthorized"}), 403

        data = request.json
        coin = data.get("coin")
        roi = data.get("roi")
        entry = data.get("entry")
        note = data.get("note", "")

        if not coin or not roi or not entry:
            return jsonify({"error": "Missing fields"}), 400

        # Format message
        message = f"🚨 SNIPER ALERT\n\n🪙 Coin: {coin}\n💰 Entry: {entry}\n🎯 Target ROI: {roi}\n📝 {note}"

        # Telegram sendMessage URL
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        # Payload with safe encoding and parse_mode
        payload = {
            "chat_id": CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML"  # Optional, emojis are fine without this too
        }

        # Send to Telegram
        response = requests.post(telegram_url, json=payload)
        response.raise_for_status()

        return jsonify({"status": "sent", "message": message})

    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Telegram error: {req_err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
