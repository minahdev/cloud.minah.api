from __future__ import annotations

from pydantic import BaseModel


class JudgeSchema(BaseModel):
    """심판(Judge) 자기소개 입력."""

    id: int
    name: str
