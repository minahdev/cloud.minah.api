from __future__ import annotations

import logging

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from comm_agent.adapter.outbound.orm.push_subscription_orm import PushSubscriptionOrm
from comm_agent.app.dtos.push_dto import PushSubscriptionCommand, PushSubscriptionInfo
from comm_agent.app.ports.output.push_subscription_port import PushSubscriptionRepositoryPort

logger = logging.getLogger(__name__)


class PushSubscriptionRepository(PushSubscriptionRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_subscription(self, command: PushSubscriptionCommand) -> None:
        # 같은 endpoint 재구독은 키 갱신 (upsert)
        await self.session.execute(
            insert(PushSubscriptionOrm)
            .values(endpoint=command.endpoint, p256dh=command.p256dh, auth=command.auth)
            .on_conflict_do_update(
                index_elements=["endpoint"],
                set_={"p256dh": command.p256dh, "auth": command.auth},
            )
        )
        await self.session.commit()

    async def list_subscriptions(self) -> list[PushSubscriptionInfo]:
        result = await self.session.execute(select(PushSubscriptionOrm))
        rows = result.scalars().all()
        return [
            PushSubscriptionInfo(endpoint=r.endpoint, p256dh=r.p256dh, auth=r.auth)
            for r in rows
        ]

    async def delete_by_endpoint(self, endpoint: str) -> None:
        await self.session.execute(
            delete(PushSubscriptionOrm).where(PushSubscriptionOrm.endpoint == endpoint)
        )
        await self.session.commit()
