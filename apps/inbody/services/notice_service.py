from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.dates import iso_utc
from inbody.models.notice_model import Notice
from inbody.repositories.notice_repository import NoticeRepository
from inbody.schemas.notice_schema import NoticeCreate, NoticeResponse
from inbody.user_lookup import require_user
from secom.app.dtos.user_model import User


def _to_response(row: Notice, author_login_id: str) -> NoticeResponse:
    return NoticeResponse(
        id=str(row.id),
        title=row.title,
        body=row.body,
        authorId=author_login_id,
        createdAt=iso_utc(row.created_at),
    )


class NoticeService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = NoticeRepository(session)
        self._session = session

    async def _login_id_for(self, user_pk: int) -> str:
        stmt = select(User.user_id).where(User.id == user_pk)
        result = await self._session.execute(stmt)
        login = result.scalar_one_or_none()
        return login or "unknown"

    async def list_notices(self) -> list[NoticeResponse]:
        rows = await self._repo.list_all()
        out: list[NoticeResponse] = []
        for row in rows:
            login = await self._login_id_for(row.author_user_id)
            out.append(_to_response(row, login))
        return out

    async def create_notice(self, payload: NoticeCreate) -> NoticeResponse:
        user = await require_user(self._session, payload.userId)
        if user.role != "admin":
            raise ValueError("관리자만 공지를 등록할 수 있습니다.")
        row = await self._repo.create(user.id, payload.title.strip(), payload.body.strip())
        return _to_response(row, user.user_id)

    async def delete_notice(self, login_user_id: str, notice_id: str) -> None:
        user = await require_user(self._session, login_user_id)
        if user.role != "admin":
            raise ValueError("관리자만 공지를 삭제할 수 있습니다.")
        try:
            pk = int(notice_id)
        except ValueError as e:
            raise ValueError("잘못된 공지 ID입니다.") from e
        ok = await self._repo.delete(pk)
        if not ok:
            raise ValueError("공지를 찾을 수 없습니다.")
