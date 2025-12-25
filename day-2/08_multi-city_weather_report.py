import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


# Environment variable for API key
API_KEY = os.getenv("OPENWEATHER_API_KEY")
def get_weather(city):
    """Get weather for a city"""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric"  # Celsius
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Invalid API key")
        elif e.response.status_code == 404:
            print(f"City not found: {city}")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None



#Read city list from a txt file, one at per line with 1 second delay
with open("cities.txt", "r") as f:
    cities = [line.strip() for line in f.readlines() if line.strip()]

max_retries = 3
successes = 0
failures = 0


for city in cities:
    attempts = 0
    weather = None

    while attempts < max_retries and weather is None:
        weather = get_weather(city)
        if weather is None:
            attempts += 1

    if weather:
        successes += 1
        print(f"{city}: {weather['main']['temp']}°C")
    else:
        failures += 1
        print(f"Failed to fetch weather for {city}")
    time.sleep(1)  # Delay between requests

#Summary report
print("\nSummary Report")
print(f"Total cities: {len(cities)}")
print(f"Successful fetches: {successes}")
print(f"Failed fetches: {failures}")

    