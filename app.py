import os
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
def convert_to_hindi_words(num):
    ones = ["", "एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ"]
    tens = ["", "दस", "बीस", "तीस", "चालीस", "पचास", "साठ", "सत्तर", "अस्सी", "नब्बे"]
    hundreds = ["", "एक सौ", "दो सौ", "तीन सौ", "चार सौ", "पाँच सौ", "छह सौ", "सात सौ", "आठ सौ", "नौ सौ"]
    
    num = int(num)

    if num == 0:
        return "शून्य"
    
    parts = []
    
    thousand = num // 1000
    num %= 1000
    if thousand > 0:
        parts.append(ones[thousand] + " हजार")

    hundred = num // 100
    num %= 100
    if hundred > 0:
        parts.append(hundreds[hundred])

    if num < 10:
        parts.append(ones[num])
    elif num < 100:
        parts.append(tens[num // 10] + (" " + ones[num % 10] if num % 10 != 0 else ""))
    
    return " ".join(filter(None, parts))

def home():
    return "Twilio OTP Voice API (Hindi) is running!"

@app.route('/send-otp', methods=['GET'])
def send_otp():
    phone = request.args.get("phone")
    otp = request.args.get("otp")  # Take OTP from user input (MIT App Inventor)
    phone = "+91" + phone
    if not phone or not otp:
        return jsonify({"error": "Phone number and OTP are required"}), 400

    otp_hindi = convert_to_hindi_words(otp)  # Convert to Hindi words

    # TwiML response for the voice call
    twiml_response = f"""
    <Response>
        <Say language="hi-IN">नमस्ते! आपका ओ.टी.पी {otp_hindi} है। धन्यवाद!</Say>
    </Response>
    """

    call = client.calls.create(
        twiml=twiml_response,
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )

    return jsonify({"success": True, "otp": otp, "call_sid": call.sid})

if __name__ == "__main__":
    app.run(debug=True)
