
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load .env file (local use)
load_dotenv()

# ===== TWILIO CREDENTIALS (FROM ENV) =====
#ACCOUNT_SID = os.getenv("AC69b588c6d03e3da1c423aa3d07ef9ad1")
#AUTH_TOKEN = os.getenv("b506cd068ac6d495a82a421673c6da2c")

# ===== WHATSAPP NUMBERS =====
#FROM_WHATSAPP = os.getenv("whatsapp:+14155238886")   # example: whatsapp:+14155238886
TO_WHATSAPP = os.getenv("whatsapp:+919342836527")       # example: whatsapp:+91XXXXXXXXXX

def send_whatsapp_message(message_body):
    """
    Send a WhatsApp message using Twilio.
    Returns True if sent successfully, False otherwise.
    """
    if not ACCOUNT_SID or not AUTH_TOKEN or not FROM_WHATSAPP or not TO_WHATSAPP:
        print("⚠️ Twilio credentials not found. Running in demo mode.")
        print(f"Demo: Would send message: {message_body}")
        return False

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP
        )
        print("✅ WhatsApp message sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")
        return False

# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    # Test with dust alert
    dust_detected = True   # change to False to test

    if dust_detected:
        send_whatsapp_message("🚨 ALERT: Dust detected on solar panel. Please clean immediately.")
    else:
        print("ℹ️ No dust detected. No message sent.")
