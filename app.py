import os
import requests
import time
from dotenv import load_dotenv
from alerts import get_air_raid_alert_status 

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.json()

def main():
    previous_status = "no_alert"  # Initialize to track status changes

    while True:
        # Fetch current alert status
        current_status = get_air_raid_alert_status(31)
        
        # Check if the status has changed
        if current_status != previous_status:
            # Send message on status change
            if current_status == "alert":
                send_message("🚨 Оголошено тривогу в м. Києві!")
            elif current_status == "no_alert":
                send_message("✅ Відбій повітряної тривоги.")
            
            # Update previous status
            previous_status = current_status

        # Wait for 20-30 seconds before checking again
        time.sleep(20)


if __name__ == "__main__":
    main()