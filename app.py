from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# TEMP: Replacing Telegram API with webhook.site for testing
WEBHOOK_TEST_URL = "https://webhook.site/403185d7-da47-45cf-8135-0522a7e368c6"

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

        message = f"🚨 SNIPER ALERT\n\n🪙 Coin: {coin}\n💰 Entry: {entry}\n📈 Target ROI: {roi}\n📝 {note}"

        # Send message to webhook.site for now
        payload = {
            "message": message
        }

        response = requests.post(WEBHOOK_TEST_URL, json=payload)
        print(f"Webhook.site response: {response.status_code} - {response.text}")

        return jsonify({"status": "sent", "message": message})

    except Exception as e:
        print(f"Error in /signal: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
