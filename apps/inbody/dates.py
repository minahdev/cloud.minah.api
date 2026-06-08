from datetime import date, datetime, timezone


def parse_date_key(value: str | None) -> date:
    if not value or not value.strip():
        return datetime.now(timezone.utc).date()
    raw = value.strip()[:10]
    return date.fromisoformat(raw)


def iso_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")
