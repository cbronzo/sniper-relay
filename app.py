from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
BOT_ALIAS = os.getenv("BOT_ALIAS", "Sniper")
SNIPER_SECRET = os.getenv("SNIPER_SECRET", "none")

@app.route("/")
def home():
    return "Sniper Relay is live and protected!"

@app.route("/signal", methods=["POST"])
def sniper_signal():
    try:
        # 🔐 Require secret key as a query param
        auth_key = request.args.get("key")
        if auth_key != SNIPER_SECRET:
            print("❌ Unauthorized attempt to access /signal")
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json(force=True)
        print(f"🔥 SIGNAL RECEIVED: {data}")

        coin = data.get("coin", "UNKNOWN")
        roi = data.get("roi", "N/A")
        entry = data.get("entry", "N/A")
        note = data.get("note", "")

        message = (
            f"🚨 {BOT_ALIAS} SNIPER ALERT\n\n"
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
        print(f"📬 Telegram API Response: {response.status_code} - {response.text}")

        return jsonify({"status": "sent", "message": message})

    except Exception as e:
        print(f"❌ Error in /signal: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
