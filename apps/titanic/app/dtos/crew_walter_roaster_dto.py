from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass


if TYPE_CHECKING:
    from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema


@dataclass
class WalterRoasterQuery:
    """WalterRoasterSchema → 앱 레이어 전달용 (타입은 str 통일)."""

    id: str
    name: str



@dataclass
class WalterRoasterResponse:
    id: int
    name: str

