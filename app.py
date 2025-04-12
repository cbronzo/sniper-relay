from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 Your hardcoded secrets
BOT_TOKEN = "7876168717:AAEZG9J10w9HjyHLYAF4F25REgNS01KLZcc"
CHAT_ID = "-1002502682234"  # This is your channel ID
SNIPER_SECRET = "moonaccess123"

# ✅ Test route to confirm deployment
@app.route("/test", methods=["GET"])
def test_route():
    return "✅ App is live and responding"

# 📤 Main endpoint to send sniper alerts
@app.route("/send", methods=["POST"])
def send_alert():
    try:
        data = request.get_json()

        # 🔐 Optional: verify sniper secret
        secret = data.get("secret")
        if secret != SNIPER_SECRET:
            return jsonify({"error": "Unauthorized"}), 403

        message = data.get("message", "⚠️ Default test message")

        print("🔄 Attempting to send Telegram message...")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(url, data=payload)
        print(f"🔧 Status Code: {response.status_code}")
        print(f"🧾 Response Text: {response.text}")

        if response.status_code == 200:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "fail", "response": response.text}), 500

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500

# Optional for local testing
if __name__ == "__main__":
    app.run(debug=True)
