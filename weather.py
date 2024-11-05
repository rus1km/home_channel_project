# weather.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_STATION_ID = os.getenv("WEATHER_STATION_ID")

def get_air_quality_index():
    url = f"https://www.saveecobot.com/api/v1/aqi-ukraine/sensor-last-data/{WEATHER_STATION_ID}?apikey={WEATHER_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        data = response.json()

        aqi = None
        temperature = None

        # Iterate over items in 'data' to find 'aqi_pm25' and 'temperature'
        for item in data.get("data", []):
            if item["phenomenon"] == "aqi_pm25":
                aqi = item["value"]
            elif item["phenomenon"] == "temperature":
                temperature = round(item["value"])  # Convert temperature to an integer

        # Return both values as a dictionary, handling cases where data might be missing
        return {"aqi": aqi, "temperature": temperature} if aqi is not None and temperature is not None else {"aqi": "N/D", "temperature": "N/D"}

    except requests.exceptions.RequestException as e:
        print("Error fetching air quality data:", e)
        return None