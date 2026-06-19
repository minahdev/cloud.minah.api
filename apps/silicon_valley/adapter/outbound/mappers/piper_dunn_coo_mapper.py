from __future__ import annotations

from typing import Any

from silicon_valley.adapter.outbound.orm.piper_dunn_coo_orm import DunnCooOrm


class DunnCooMapper:
    """DunnCooOrm(DB) ↔ DunnCooEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: DunnCooOrm) -> Any:
        raise NotImplementedError("DunnCooOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> DunnCooOrm:
        raise NotImplementedError("DunnCooEntity is not yet implemented")
