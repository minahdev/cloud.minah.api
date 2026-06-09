from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NoticeCreateCommand:
    user_id: str
    title: str
    body: str


@dataclass
class NoticeDeleteCommand:
    user_id: str
    notice_id: str


@dataclass
class NoticeDto:
    id: str
    title: str
    body: str
    author_id: str
    created_at: str
