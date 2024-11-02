# weather.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
LAT = float(os.getenv("LAT"))
LON = float(os.getenv("LON"))

def get_air_quality_index():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={WEATHER_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        data = response.json()
        
        # Extract AQI information from the response
        aqi = data['list'][0]['main']['aqi']  # AQI is a number from 1 to 5
        return aqi
    
    except requests.exceptions.RequestException as e:
        print("Error fetching air quality data:", e)
        return None