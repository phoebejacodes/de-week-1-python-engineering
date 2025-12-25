from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not set in .env")
    
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()

try:
    weather = get_weather("Tokyo")
    print(f"Tokyo: {weather['main']['temp']}°C")
except Exception as e:
    print(f"Error: {e}")

try:
    weather = get_weather("Kingston")
    print(f"Kingston: {weather['main']['temp']}°C")
except Exception as e:
    print(f"Error: {e}")