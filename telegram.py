# telegram.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PINNED_MESSAGE_ID = int(os.getenv("PINNED_MESSAGE_ID"))

def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.json()

def update_pinned_message(message):
    """Edit the pinned message with new information."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": CHAT_ID,
        "message_id": PINNED_MESSAGE_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.json()
