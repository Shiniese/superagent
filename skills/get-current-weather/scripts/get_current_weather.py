import argparse

import requests
import toon_format

def get_current_weather(latitude: float = 39.9042, longitude: float = 116.4074) -> str:
    """
    Get the current weather for a given location using Open-Meteo API.

    Args:
        latitude: Latitude of the location (e.g., 52.52)
        longitude: Longitude of the location (e.g., 13.41)
    """

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "weather_code,temperature_2m,wind_speed_10m,relative_humidity_2m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,wind_speed_10m_max",
        "forecast_days": 3,
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return toon_format.encode(data)
    
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"
    

def main():
    parser = argparse.ArgumentParser(description="Get current weather for a location.")
    parser.add_argument("latitude", type=float, help="Latitude of the location (e.g., 52.52)")
    parser.add_argument("longitude", type=float, help="Longitude of the location (e.g., 13.41)")
    args = parser.parse_args()
    weather = get_current_weather(args.latitude, args.longitude)
    print(weather)

if __name__ == "__main__":
    main()