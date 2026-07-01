from __future__ import annotations

from abc import ABC, abstractmethod

from comm_agent.app.dtos.push_dto import PushSubscriptionCommand, PushSubscriptionInfo


class PushSubscriptionRepositoryPort(ABC):
    """웹 푸시 구독 저장·조회 게이트웨이."""

    @abstractmethod
    async def save_subscription(self, command: PushSubscriptionCommand) -> None:
        pass

    @abstractmethod
    async def list_subscriptions(self) -> list[PushSubscriptionInfo]:
        pass

    @abstractmethod
    async def delete_by_endpoint(self, endpoint: str) -> None:
        pass
