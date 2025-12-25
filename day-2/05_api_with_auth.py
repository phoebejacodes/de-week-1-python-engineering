import requests
import os

# Never hardcode API keys! Use environment variable
API_KEY = os.environ.get("OPENWEATHER_API_KEY")

if not API_KEY:
    print("Please set OPENWEATHER_API_KEY environment variable")
    print("Run: export OPENWEATHER_API_KEY='your-key-here'")
    exit(1)

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

# Set API key in environment first:
# export OPENWEATHER_API_KEY='your-key-here'

weather = get_weather("Kingston")
if weather:
    temp = weather.get("main", {}).get("temp")
    description = weather.get("weather", [{}])[0].get("description")

    if temp is None or description is None:
        print("Weather data missing expected fields")
    else:
        print(f"City: {weather['name']}")
        print(f"Temperature: {temp}°C")
        print(f"Description: {description}")
else:
    print("Failed to retrieve weather data")