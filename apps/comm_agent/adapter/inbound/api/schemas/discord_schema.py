from __future__ import annotations

from pydantic import BaseModel


class DiscordIntroduceSchema(BaseModel):
    """Discord Agent 자기소개 입력."""

    id: int
    name: str
