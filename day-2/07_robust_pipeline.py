from dotenv import load_dotenv
import os
import requests
import json
import csv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    """Fetch weather for a single city"""
    try:
        response = requests.get(
            BASE_URL,
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp_celsius": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "fetched_at": datetime.now().isoformat()
        }
        
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP Error for {city}: {e.response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  Request failed for {city}: {e}")
        return None
    except KeyError as e:
        print(f"  Missing data for {city}: {e}")
        return None

def main():
    if not API_KEY:
        print("Error: OPENWEATHER_API_KEY not set")
        return
    
    cities = [
        "London",
        "Tokyo",
        "New York",
        "Paris",
        "Sydney",
        "Kingston",
        "InvalidCityXYZ123",  # This will fail
        "Berlin",
        "Mumbai"
    ]
    
    results = []
    failed = []
    
    print(f"Fetching weather for {len(cities)} cities...")
    
    for city in cities:
        print(f"  Fetching {city}...")
        weather = fetch_weather(city)
        
        if weather:
            results.append(weather)
            print(f"    ✓ {weather['temp_celsius']}°C")
        else:
            failed.append(city)
            print(f"    ✗ Failed")
    
    print(f"\nSuccess: {len(results)}/{len(cities)}")
    print(f"Failed: {failed}")
    
    if results:
        # Write JSON
        with open("weather_data.json", "w") as f:
            json.dump(results, f, indent=2)
        
        # Write CSV
        with open("weather_data.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\nWrote {len(results)} records to weather_data.json and weather_data.csv")

if __name__ == "__main__":
    main()