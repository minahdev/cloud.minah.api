from __future__ import annotations

from abc import ABC, abstractmethod

from comm_agent.app.dtos.push_dto import PushSubscriptionInfo


class PushSenderPort(ABC):
    """실제 웹 푸시 메시지를 발송하는 게이트웨이."""

    @abstractmethod
    async def send(self, subscription: PushSubscriptionInfo, payload: str) -> bool:
        """발송 성공 시 True. 구독 만료(410/404) 등 영구 실패는 False."""
        pass
