# utils.py
import aiohttp
from typing import Optional

BASE_URL = "https://api.open-meteo.com/v1/forecast"

async def get_coordinates(city: str) -> Optional[dict]:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            if "results" not in data or not data["results"]:
                return None
            location = data["results"][0]
            return {"lat": location["latitude"], "lon": location["longitude"]}

async def fetch_weather(city: str) -> Optional[str]:
    coordinates = await get_coordinates(city)
    if not coordinates:
        return None

    lat, lon = coordinates["lat"], coordinates["lon"]
    url = f"{BASE_URL}?latitude={lat}&longitude={lon}&current_weather=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            weather = data.get("current_weather", {})
            return f"🌤️ Weather in {city}: {weather.get('temperature')}°C, Wind {weather.get('windspeed')} km/h"