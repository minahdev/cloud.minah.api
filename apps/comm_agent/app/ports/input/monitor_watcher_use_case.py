from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from comm_agent.app.dtos.monitor_watcher_dto import MonitorWatcherResponse

if TYPE_CHECKING:
    from comm_agent.adapter.inbound.api.schemas.monitor_watcher_schema import (
        MonitorWatcherSchema,
    )
    from comm_agent.app.dtos.received_mail_dto import ReceivedMailCommand


class MonitorWatcherUseCase(ABC):
    """모니터(관찰/기록자) — 이벤트·로그·상태 변화 관찰 담당."""

    @abstractmethod
    async def introduce_myself(self, schema: MonitorWatcherSchema) -> MonitorWatcherResponse:
        pass

    @abstractmethod
    async def screen_and_store(self, command: ReceivedMailCommand) -> dict:
        """메일을 필터링해 정상건만 received_mail 파이프라인(→pgvector)으로 넘긴다."""
        pass
