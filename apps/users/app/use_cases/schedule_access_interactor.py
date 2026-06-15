import hashlib
import secrets
import string
from datetime import datetime, timedelta, timezone

import bcrypt

from users.app.ports.input.schedule_access_use_case import ScheduleAccessUseCase
from users.app.ports.output.schedule_access_repository import ScheduleAccessRepository
from users.app.ports.output.user_repository import UserRepository

_CODE_ALPHABET = string.ascii_uppercase + string.digits
_CODE_LENGTH = 8
_CODE_TTL_DAYS = 7


def _normalize_invite_code(code: str) -> str:
    return code.strip().upper().replace(" ", "").replace("-", "")


def _invite_code_digest(code: str) -> str:
    return hashlib.sha256(_normalize_invite_code(code).encode("utf-8")).hexdigest()


def _generate_plain_invite_code() -> str:
    return "".join(secrets.choice(_CODE_ALPHABET) for _ in range(_CODE_LENGTH))


class ScheduleAccessService(ScheduleAccessUseCase):
    def __init__(self, repository: ScheduleAccessRepository, user_repository: UserRepository) -> None:
        self._repo = repository
        self._users = user_repository

    async def is_configured(self) -> bool:
        """회원 스케줄 입장 제어 사용 여부 (코드 또는 구 접근 암호)."""
        row = await self._repo.get_row()
        if row and row.password_hash:
            return True
        return (await self._repo.count_active_invite_codes()) > 0

    async def is_admitted(self, user_id: str) -> bool:
        return await self._repo.is_admitted(user_id)

    async def verify_password(self, password: str) -> bool:
        row = await self._repo.get_row()
        if not row or not row.password_hash:
            return False
        return bcrypt.checkpw(
            password.encode("utf-8"),
            row.password_hash.encode("utf-8"),
        )

    async def verify_and_grant(self, user_id: str, password: str) -> None:
        user = await self._users.find_by_user_id(user_id)
        if user is None:
            raise ValueError("사용자를 찾을 수 없습니다.")
        if user.role != "user":
            raise ValueError("회원만 입장 코드를 사용할 수 있습니다.")
        if not await self.verify_password(password):
            raise ValueError("접근 암호가 올바르지 않습니다.")
        await self._repo.grant_user(user_id)

    async def create_invite_code(self, coach_user_id: str) -> dict[str, str]:
        user = await self._users.find_by_user_id(coach_user_id)
        if user is None:
            raise ValueError("사용자를 찾을 수 없습니다.")
        if user.role not in ("coach", "admin"):
            raise ValueError("코치 또는 관리자만 입장 코드를 발급할 수 있습니다.")

        plain = _generate_plain_invite_code()
        expires_at = datetime.now(timezone.utc) + timedelta(days=_CODE_TTL_DAYS)
        await self._repo.create_invite_code(
            _invite_code_digest(plain),
            coach_user_id,
            expires_at,
            max_uses=1,
        )
        return {
            "code": plain,
            "expiresAt": expires_at.isoformat().replace("+00:00", "Z"),
        }

    async def redeem_invite_code(self, user_id: str, code: str) -> None:
        user = await self._users.find_by_user_id(user_id)
        if user is None:
            raise ValueError("사용자를 찾을 수 없습니다.")
        if user.role != "user":
            raise ValueError("회원만 입장 코드를 사용할 수 있습니다.")

        normalized = _normalize_invite_code(code)
        if len(normalized) < 6:
            raise ValueError("입장 코드 형식이 올바르지 않습니다.")

        invite = await self._repo.find_redeemable_invite(_invite_code_digest(normalized))
        if invite is None:
            raise ValueError("입장 코드가 올바르지 않거나 만료·사용되었습니다.")

        await self._repo.mark_invite_used(invite.id)
        await self._repo.grant_user(user_id)

    async def require_member_admitted(self, login_user_id: str) -> None:
        user = await self._users.find_by_user_id(login_user_id)
        if user is None:
            raise ValueError("사용자를 찾을 수 없습니다.")
        if user.role in ("coach", "admin"):
            return
        if not await self.is_admitted(login_user_id):
            raise ValueError("스케줄 입장 코드를 입력한 회원만 레슨을 이용할 수 있습니다.")

    async def set_password(self, coach_user_id: str, password: str) -> None:
        user = await self._users.find_by_user_id(coach_user_id)
        if user is None:
            raise ValueError("사용자를 찾을 수 없습니다.")
        if user.role not in ("coach", "admin"):
            raise ValueError("코치 또는 관리자만 접근 암호를 설정할 수 있습니다.")
        if len(password) < 4:
            raise ValueError("접근 암호는 4자 이상으로 설정해 주세요.")

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")
        await self._repo.upsert_password(password_hash, coach_user_id)
        await self._repo.clear_grants()

    async def list_admitted_members_for_coach(self, requester_user_id: str) -> list[dict[str, str]]:
        requester = await self._users.find_by_user_id(requester_user_id)
        if requester is None:
            raise ValueError("사용자를 찾을 수 없습니다.")
        if requester.role not in ("coach", "admin"):
            raise ValueError("코치 또는 관리자만 회원 목록을 조회할 수 있습니다.")
        rows = await self._repo.list_admitted_members()
        return [{"userId": uid, "nickname": nick} for uid, nick in rows]
