from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Mini Bot Live"

@app.route("/test", methods=["GET"])
def test_direct_send():
    try:
        telegram_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
        payload = {
            "chat_id": os.getenv("TELEGRAM_CHANNEL_ID"),
            "text": "🚨 Auto-fire test via Railway direct call"
        }
        r = requests.post(telegram_url, json=payload)
        r.raise_for_status()
        return jsonify({"status": "sent"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
