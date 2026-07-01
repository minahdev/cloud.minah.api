from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from comm_agent.adapter.outbound.orm.received_mail_orm import ReceivedMailOrm
from comm_agent.app.dtos.received_mail_dto import ReceivedMailCommand, ReceivedMailView
from comm_agent.app.ports.output.received_mail_port import ReceivedMailRepositoryPort

logger = logging.getLogger(__name__)


class ReceivedMailRepository(ReceivedMailRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_mail(self, command: ReceivedMailCommand) -> int:
        orm = ReceivedMailOrm(
            sender=command.sender,
            subject=command.subject,
            body=command.body,
        )
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return orm.id

    async def list_mails(self) -> list[ReceivedMailView]:
        result = await self.session.execute(
            select(ReceivedMailOrm).order_by(ReceivedMailOrm.received_at.desc())
        )
        rows = result.scalars().all()
        return [
            ReceivedMailView(
                id=row.id,
                sender=row.sender,
                subject=row.subject,
                body=row.body,
                received_at=row.received_at.isoformat(),
            )
            for row in rows
        ]
