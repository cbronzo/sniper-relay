from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hardcoded for test only
BOT_TOKEN = "7876168717:AAEZG9J10w9HjyHLYAF4F25REgNSO1KLZcc"
CHANNEL_ID = "-1002502682234"

@app.route("/")
def home():
    return "Hardcoded Mini Bot Live"

@app.route("/test", methods=["GET"])
def test_direct_send():
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": "🚨 Hardcoded test message — should appear now"
        }
        r = requests.post(telegram_url, json=payload)
        r.raise_for_status()
        return jsonify({"status": "sent"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
