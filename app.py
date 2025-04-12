from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Get environment variables from Railway
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
BOT_ALIAS = os.getenv("BOT_ALIAS", "Sniper Elite")
SNIPER_SECRET = os.getenv("SNIPER_SECRET")

@app.route("/")
def home():
    return f"{BOT_ALIAS} Relay is active!"

@app.route("/signal", methods=["POST"])
def sniper_signal():
    try:
        # --- AUTHENTICATION ---
        auth_key = request.args.get("key")
        if auth_key != SNIPER_SECRET:
            print("❌ Unauthorized access attempt. Provided key:", auth_key)
            return jsonify({"error": "Unauthorized"}), 403

        # --- PARSE REQUEST ---
        data = request.get_json(force=True)
        print("🔥 Received data:", data)

        coin = data.get("coin")
        roi = data.get("roi")
        entry = data.get("entry")
        note = data.get("note", "")

        if not coin or not roi or not entry:
            print("❌ Missing required fields in data:", data)
            return jsonify({"error": "Missing required fields"}), 400

        # --- BUILD MESSAGE ---
        message = (
            f"🚨 {BOT_ALIAS} ALERT\n\n"
            f"🪙 Coin: {coin}\n"
            f"💰 Entry: {entry}\n"
            f"📈 Target ROI: {roi}\n"
            f"📝 {note}"
        )
        print("📬 Message to send:", message)

        # --- SEND TO TELEGRAM ---
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": message
        }
        response = requests.post(telegram_url, json=payload)
        print("📬 Telegram API response:", response.status_code, response.text)
        response.raise_for_status()

        return jsonify({"status": "sent", "message": message}), 200

    except Exception as e:
        print("❌ Error in /signal:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print("Starting app on port", port)
    app.run(host="0.0.0.0", port=port)
