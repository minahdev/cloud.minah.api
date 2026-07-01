from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from comm_agent.app.dtos.monitor_watcher_dto import MonitorWatcherResponse

if TYPE_CHECKING:
    from comm_agent.adapter.inbound.api.schemas.monitor_watcher_schema import (
        MonitorWatcherSchema,
    )


class MonitorWatcherUseCase(ABC):
    """모니터(관찰/기록자) — 이벤트·로그·상태 변화 관찰 담당."""

    @abstractmethod
    async def introduce_myself(self, schema: MonitorWatcherSchema) -> MonitorWatcherResponse:
        pass
