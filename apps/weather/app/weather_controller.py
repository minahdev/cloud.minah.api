from core.matrix.secret_manager import Keymaker, get_keymaker

from weather.app.weather_service import WeatherService


class WeatherController:
    """날씨 API 진입점 (좌표·도시)."""

    def __init__(self, keymaker: Keymaker | None = None) -> None:
        km = keymaker or get_keymaker()
        self._service = WeatherService(km)

    def get_by_coordinates(self, lat: float, lon: float) -> dict:
        return self._service.fetch_by_coords(lat, lon)

    def get_by_city(self, city: str) -> dict:
        return self._service.fetch_by_city(city)
