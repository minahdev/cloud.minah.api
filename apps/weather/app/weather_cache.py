"""OpenWeather 응답 단기 캐시 (느린 외부 API 대비)."""

from __future__ import annotations

import time

_TTL_SEC = 600
_cache: dict[str, tuple[float, dict]] = {}


def cache_key(*, lat: float | None = None, lon: float | None = None, city: str | None = None) -> str:
    if lat is not None and lon is not None:
        return f"coord:{round(lat, 4)}:{round(lon, 4)}"
    return f"city:{(city or '').strip().lower()}"


def get_cached(key: str) -> dict | None:
    row = _cache.get(key)
    if not row:
        return None
    expires_at, payload = row
    if time.monotonic() > expires_at:
        _cache.pop(key, None)
        return None
    return payload


def set_cached(key: str, payload: dict) -> None:
    _cache[key] = (time.monotonic() + _TTL_SEC, payload)
