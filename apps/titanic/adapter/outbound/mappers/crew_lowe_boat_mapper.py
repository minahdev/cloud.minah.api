from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.crew_lowe_boat_orm import LoweBoatOrm


class LoweBoatMapper:
    """LoweBoatOrm(DB) ↔ LoweBoatEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: LoweBoatOrm) -> Any:
        raise NotImplementedError("LoweBoatOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> LoweBoatOrm:
        raise NotImplementedError("LoweBoatEntity is not yet implemented")
