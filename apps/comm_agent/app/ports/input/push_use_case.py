from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from comm_agent.app.dtos.push_dto import PushResponse, PushSubscriptionCommand

if TYPE_CHECKING:
    from comm_agent.adapter.inbound.api.schemas.push_schema import (
        PushIntroduceSchema,
    )


class PushUseCase(ABC):
    """웹 푸시 구독 등록·전체 발송."""

    @abstractmethod
    async def subscribe(self, command: PushSubscriptionCommand) -> None:
        pass

    @abstractmethod
    async def notify_all(self, title: str, body: str) -> int:
        """등록된 모든 구독에 알림을 보내고, 성공 건수를 돌려준다."""
        pass

    @abstractmethod
    async def introduce_myself(self, schema: PushIntroduceSchema) -> PushResponse:
        pass
