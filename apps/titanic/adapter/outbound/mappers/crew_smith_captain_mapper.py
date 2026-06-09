from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.crew_smith_captain_orm import SmithCaptainOrm


class SmithCaptainMapper:
    """SmithCaptainOrm(DB) ↔ SmithCaptainEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: SmithCaptainOrm) -> Any:
        raise NotImplementedError("SmithCaptainOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> SmithCaptainOrm:
        raise NotImplementedError("SmithCaptainEntity is not yet implemented")
