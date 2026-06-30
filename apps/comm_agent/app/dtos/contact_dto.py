from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContactCommand:
    """주소록 저장 입력 1건."""

    nickname: str
    email: str


@dataclass
class ContactView:
    """주소록 조회 결과 1건."""

    id: int
    nickname: str
    email: str
