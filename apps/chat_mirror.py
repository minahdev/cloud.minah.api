"""프론트 Gemini 채팅과 동기화할 최근 대화 (인메모리)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass
class LastChatSnapshot:
    user_text: str
    model_text: str
    model_name: str | None = None
    updated_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


_last: LastChatSnapshot | None = None


def record_chat(user_text: str, model_text: str, model_name: str | None = None) -> None:
    global _last
    _last = LastChatSnapshot(
        user_text=user_text.strip(),
        model_text=model_text.strip(),
        model_name=model_name,
        updated_at=datetime.now(timezone.utc).isoformat(),
    )


def get_last_chat() -> LastChatSnapshot | None:
    return _last
