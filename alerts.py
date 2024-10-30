# alerts.py
import os
from dotenv import load_dotenv
from alerts_in_ua import Client as AlertsClient

# Load environment variables from .env file
load_dotenv()

ALERTS_API_KEY = os.getenv("ALERTS_API_KEY")

# location UID can be found here https://devs.alerts.in.ua
def get_air_raid_alert_status(region=None):
    alerts_client = AlertsClient(token=ALERTS_API_KEY)
    if region:
        return alerts_client.get_air_raid_alert_status(region)
    return alerts_client.get_air_raid_alert_status()