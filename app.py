from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 Replace these with your real bot token + chat ID
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"  # for groups it might be like -1001234567890

# ✅ Test route to verify app is up
@app.route("/test", methods=["GET"])
def test_route():
    return "✅ App is live and responding"

# 📤 Main route to send a Telegram message
@app.route("/send", methods=["POST"])
def send_alert():
    try:
        data = request.get_json()
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

# 🔁 Needed to run locally (won’t be used by Railway, but safe to leave in)
if __name__ == "__main__":
    app.run(debug=True)
