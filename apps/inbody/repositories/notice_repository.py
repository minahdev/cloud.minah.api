from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.models.notice_model import Notice


class NoticeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Notice]:
        stmt = select(Notice).order_by(Notice.created_at.desc())
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, author_user_id: int, title: str, body: str) -> Notice:
        row = Notice(
            author_user_id=author_user_id,
            title=title,
            body=body,
            created_at=datetime.now(timezone.utc),
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return row

    async def delete(self, notice_id: int) -> bool:
        stmt = select(Notice).where(Notice.id == notice_id)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            return False
        await self._session.delete(row)
        await self._session.commit()
        return True
