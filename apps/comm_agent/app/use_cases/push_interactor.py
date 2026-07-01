from __future__ import annotations

import json
import logging

from comm_agent.app.dtos.push_dto import PushSubscriptionCommand
from comm_agent.app.ports.input.push_use_case import PushUseCase
from comm_agent.app.ports.output.push_sender_port import PushSenderPort
from comm_agent.app.ports.output.push_subscription_port import PushSubscriptionRepositoryPort

logger = logging.getLogger(__name__)


class PushInteractor(PushUseCase):
    def __init__(
        self,
        repository: PushSubscriptionRepositoryPort,
        sender: PushSenderPort,
    ) -> None:
        self._repository = repository
        self._sender = sender

    async def subscribe(self, command: PushSubscriptionCommand) -> None:
        await self._repository.save_subscription(command)
        logger.info("[Push] 구독 등록 | endpoint=%s...", command.endpoint[:40])

    async def notify_all(self, title: str, body: str) -> int:
        subscriptions = await self._repository.list_subscriptions()
        if not subscriptions:
            return 0
        payload = json.dumps({"title": title, "body": body, "url": "/inbox"})
        sent = 0
        for sub in subscriptions:
            ok = await self._sender.send(sub, payload)
            if ok:
                sent += 1
            else:
                # 만료/실패한 구독은 정리
                await self._repository.delete_by_endpoint(sub.endpoint)
        logger.info("[Push] 발송 | 대상=%d 성공=%d", len(subscriptions), sent)
        return sent
