import os

import httpx

from matrix.app.keymaker import Keymaker

_OPENWEATHER_BASE = "https://api.openweathermap.org/data/2.5/weather"


class WeatherService:
    """OpenWeatherMap 현재 날씨 조회."""

    def __init__(self, keymaker: Keymaker) -> None:
        self._keymaker = keymaker

    def _api_key(self) -> str:
        return self._keymaker.get_weather_api_key()

    def _normalize(self, data: dict) -> dict:
        weather = (data.get("weather") or [{}])[0]
        main = data.get("main") or {}
        return {
            "city": (data.get("name") or "").strip() or "Unknown",
            "temp_c": main.get("temp"),
            "feels_like_c": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "description": weather.get("description", ""),
            "icon": weather.get("icon"),
            "lat": data.get("coord", {}).get("lat"),
            "lon": data.get("coord", {}).get("lon"),
        }

    def fetch_by_coords(self, lat: float, lon: float) -> dict:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self._api_key(),
            "units": "metric",
            "lang": os.getenv("WEATHER_LANG", "kr"),
        }
        with httpx.Client(timeout=15.0) as client:
            res = client.get(_OPENWEATHER_BASE, params=params)
            res.raise_for_status()
            return self._normalize(res.json())

    def fetch_by_city(self, city: str) -> dict:
        params = {
            "q": city.strip(),
            "appid": self._api_key(),
            "units": "metric",
            "lang": os.getenv("WEATHER_LANG", "kr"),
        }
        with httpx.Client(timeout=15.0) as client:
            res = client.get(_OPENWEATHER_BASE, params=params)
            res.raise_for_status()
            return self._normalize(res.json())
