from __future__ import annotations

import logging

from comm_agent.adapter.inbound.api.schemas.monitor_watcher_schema import (
    MonitorWatcherSchema,
)
from comm_agent.app.dtos.monitor_watcher_dto import MonitorWatcherQuery, MonitorWatcherResponse
from comm_agent.app.dtos.received_mail_dto import ReceivedMailCommand
from comm_agent.app.ports.input.monitor_watcher_use_case import MonitorWatcherUseCase
from comm_agent.app.ports.input.received_mail_use_case import ReceiveMailUseCase
from comm_agent.app.ports.output.monitor_watcher_port import MonitorWatcherPort
from comm_agent.app.ports.output.spam_filter_port import SpamFilterPort

logger = logging.getLogger(__name__)


class MonitorWatcherInteractor(MonitorWatcherUseCase):
    """왓슨 Triage 관문 — 인입 메일을 필터링해 정상건만 통과시킨다."""

    def __init__(
        self,
        repository: MonitorWatcherPort,
        spam_filter: SpamFilterPort,
        receive_mail: ReceiveMailUseCase,
    ) -> None:
        self._repository = repository
        self._spam_filter = spam_filter
        self._receive_mail = receive_mail

    async def introduce_myself(self, schema: MonitorWatcherSchema) -> MonitorWatcherResponse:
        return await self._repository.introduce_myself(
            MonitorWatcherQuery(id=schema.id, name=schema.name)
        )

    async def screen_and_store(self, command: ReceivedMailCommand) -> dict:
        # 제목+본문을 KcELECTRA 필터로 판정 → 정상만 received_mail 파이프라인(→pgvector)으로 전달
        content = f"{command.subject}\n\n{command.body}".strip()
        verdict = await self._spam_filter.classify(content)

        if not verdict.is_normal:
            logger.warning(
                "[MonitorWatcher] 🚫 비정상 메일 차단 | label=%s | from=%s",
                verdict.label,
                command.sender,
            )
            return {"stored": False, "blocked": True, "label": verdict.label}

        mail_id = await self._receive_mail.save_incoming(command)
        logger.info("[MonitorWatcher] ✅ 정상 메일 통과 → pgvector 저장 | id=%s", mail_id)
        return {"stored": True, "id": mail_id, "label": verdict.label}
