from __future__ import annotations

import logging

from sqlalchemy import or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from comm_agent.adapter.outbound.orm.contact_orm import ContactOrm
from comm_agent.app.dtos.contact_dto import ContactCommand, ContactView
from comm_agent.app.ports.output.contact_port import ContactRepositoryPort

logger = logging.getLogger(__name__)


class ContactRepository(ContactRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_contacts(self, commands: list[ContactCommand]) -> int:
        values = [{"nickname": c.nickname, "email": c.email} for c in commands if c.email]
        if not values:
            return 0
        # 같은 이메일은 무시 (중복 업로드 안전)
        await self.session.execute(
            insert(ContactOrm).values(values).on_conflict_do_nothing(index_elements=["email"])
        )
        await self.session.commit()
        return len(values)

    async def list_contacts(self) -> list[ContactView]:
        result = await self.session.execute(select(ContactOrm).order_by(ContactOrm.nickname))
        rows = result.scalars().all()
        return [
            ContactView(id=row.id, nickname=row.nickname or "", email=row.email)
            for row in rows
        ]

    async def search_contacts(self, keyword: str) -> list[ContactView]:
        kw = (keyword or "").strip()
        if not kw:
            return []
        pattern = f"%{kw}%"
        stmt = (
            select(ContactOrm)
            .where(
                or_(
                    ContactOrm.nickname.ilike(pattern),
                    ContactOrm.email.ilike(pattern),
                    ContactOrm.first_name.ilike(pattern),
                    ContactOrm.last_name.ilike(pattern),
                    ContactOrm.file_as.ilike(pattern),
                )
            )
            .order_by(ContactOrm.nickname)
            .limit(20)
        )
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        return [
            ContactView(id=row.id, nickname=row.nickname or "", email=row.email)
            for row in rows
        ]
