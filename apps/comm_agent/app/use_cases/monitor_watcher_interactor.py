from __future__ import annotations

import logging

from comm_agent.adapter.inbound.api.schemas.monitor_watcher_schema import (
    MonitorWatcherSchema,
)
from comm_agent.app.dtos.monitor_watcher_dto import MonitorWatcherResponse
from comm_agent.app.ports.input.monitor_watcher_use_case import MonitorWatcherUseCase

logger = logging.getLogger(__name__)


class MonitorWatcherInteractor(MonitorWatcherUseCase):
    async def introduce_myself(self, schema: MonitorWatcherSchema) -> MonitorWatcherResponse:
        logger.info("[MonitorWatcher] introduce_myself | id=%s name=%s", schema.id, schema.name)
        return MonitorWatcherResponse(
            id=schema.id,
            name=schema.name,
            answer=(
                f"안녕하세요, 저는 '{schema.name}'입니다. "
                "시스템의 이벤트·로그·상태 변화를 관찰하고 기록합니다."
            ),
        )
