from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InbodyUserDto:
    id: int
    user_id: str
    role: str
