from __future__ import annotations

from typing import Any

from silicon_valley.adapter.outbound.orm.piper_bighetti_hr_orm import BighettiHrOrm


class BighettiHrMapper:
    """BighettiHrOrm(DB) ↔ BighettiHrEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: BighettiHrOrm) -> Any:
        raise NotImplementedError("BighettiHrOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> BighettiHrOrm:
        raise NotImplementedError("BighettiHrEntity is not yet implemented")
