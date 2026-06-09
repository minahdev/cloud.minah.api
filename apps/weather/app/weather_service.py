import os

import httpx

from core.matrix.secret_manager import Keymaker
from weather.app.weather_cache import cache_key, get_cached, set_cached

_OPENWEATHER_BASE = "https://api.openweathermap.org/data/2.5/weather"
_HTTP_TIMEOUT = httpx.Timeout(5.0, connect=3.0)


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

    def _fetch(self, params: dict, *, lat: float | None, lon: float | None, city: str | None) -> dict:
        key = cache_key(lat=lat, lon=lon, city=city)
        cached = get_cached(key)
        if cached is not None:
            return cached

        with httpx.Client(timeout=_HTTP_TIMEOUT) as client:
            res = client.get(_OPENWEATHER_BASE, params=params)
            res.raise_for_status()
            payload = self._normalize(res.json())
        set_cached(key, payload)
        return payload

    def fetch_by_coords(self, lat: float, lon: float) -> dict:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self._api_key(),
            "units": "metric",
            "lang": os.getenv("WEATHER_LANG", "ko"),
        }
        return self._fetch(params, lat=lat, lon=lon, city=None)

    def fetch_by_city(self, city: str) -> dict:
        name = city.strip()
        params = {
            "q": name,
            "appid": self._api_key(),
            "units": "metric",
            "lang": os.getenv("WEATHER_LANG", "ko"),
        }
        return self._fetch(params, lat=None, lon=None, city=name)
