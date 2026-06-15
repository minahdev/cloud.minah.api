from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.adapter.outbound.orm.notice_orm import Notice
from inbody.app.dtos.notice_dto import NoticeDto
from inbody.app.ports.output.notice_repository import NoticeRepository


def _to_dto(row: Notice) -> NoticeDto:
    return NoticeDto(
        id=str(row.id),
        title=row.title,
        body=row.body,
        author_id=str(row.author_user_id),
        created_at=row.created_at.isoformat() if row.created_at else "",
    )


class NoticePgRepository(NoticeRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[NoticeDto]:
        stmt = select(Notice).order_by(Notice.created_at.desc())
        result = await self._session.execute(stmt)
        return [_to_dto(r) for r in result.scalars().all()]

    async def create(self, author_user_pk: int, title: str, body: str) -> NoticeDto:
        row = Notice(
            author_user_id=author_user_pk,
            title=title,
            body=body,
            created_at=datetime.now(timezone.utc),
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _to_dto(row)

    async def delete(self, notice_pk: int) -> bool:
        stmt = select(Notice).where(Notice.id == notice_pk)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            return False
        await self._session.delete(row)
        await self._session.commit()
        return True
