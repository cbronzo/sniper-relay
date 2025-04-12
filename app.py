from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔒 Hardcoded values
BOT_TOKEN = "7876168717:AAEZG9J10w9HjyHLYAF4F25REgNSO1KLZcc"
CHANNEL_ID = "-1002502682234"

@app.route("/")
def home():
    return "Sniper Relay is live and hardcoded."

@app.route("/signal", methods=["POST"])
def sniper_signal():
    try:
        data = request.json
        coin = data.get("coin", "Unknown")
        roi = data.get("roi", "???")
        entry = data.get("entry", "???")
        note = data.get("note", "")

        message = f"🚨 SNIPER ALERT\n\n🪙 Coin: {coin}\n💰 Entry: {entry}\n📈 ROI Target: {roi}\n📝 {note}"

        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": message
        }

        response = requests.post(telegram_url, json=payload)
        response.raise_for_status()
        return jsonify({"status": "sent", "message": message})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Telegram error: {e}"}), 500

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
