from __future__ import annotations

from pydantic import BaseModel


class MonitorWatcherSchema(BaseModel):
    """모니터(Monitor) 자기소개 입력."""

    id: int
    name: str
