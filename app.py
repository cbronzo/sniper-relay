from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 Hardcoded secrets (yours)
BOT_TOKEN = "7876168717:AAEZG9J10w9HjyHLYAF4F25REgNS01KLZcc"
CHAT_ID = "-1002502682234"
SNIPER_SECRET = "moonaccess123"

# ✅ Test route to confirm app is running
@app.route("/test", methods=["GET"])
def test_route():
    return "✅ App is live and responding"

# 📤 Main route to receive and forward sniper alerts
@app.route("/send", methods=["POST"])
def send_alert():
    try:
        data = request.get_json()

        # 🔒 Optional secret key verification
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

# Only run locally (not on Railway)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
