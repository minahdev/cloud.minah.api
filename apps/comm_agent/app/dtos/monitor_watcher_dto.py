from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MonitorWatcherResponse:
    """모니터(Monitor) 자기소개 응답 (IntroduceResponse 대응)."""

    id: int
    name: str
    answer: str = ""
