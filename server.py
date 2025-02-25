import os
import random  # Import random module
from flask import Flask, request, jsonify
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def home():
    return "Twilio OTP API is running!"

@app.route('/send-otp', methods=['GET'])
def send_otp():
    phone = request.args.get("phone")
    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    otp = str(random.randint(1000, 9999))  # Generate a 4-digit OTP

    try:
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        return jsonify({"success": True, "otp": otp, "message_sid": message.sid})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns PORT dynamically
    app.run(host="0.0.0.0", port=port)
