# alerts.py
import os
import logging
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient

# Load environment variables from .env file
load_dotenv()

ALERTS_API_KEY = os.getenv("ALERTS_API_KEY")
CITY_UID = os.getenv("CITY_UID")

# location UID can be found here https://devs.alerts.in.ua
def get_air_raid_alert_status():
    alerts_client = AlertsClient(token=ALERTS_API_KEY)
    response = alerts_client.get_air_raid_alert_status(CITY_UID)
    logging.info(F"Alerts response: {response}")
    status = 1 if response.status == "active" else 0
    return status
