from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.passenger_molly_scaler_orm import MollyScalerOrm


class MollyScalerMapper:
    """MollyScalerOrm(DB) ↔ MollyScalerEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: MollyScalerOrm) -> Any:
        raise NotImplementedError("MollyScalerOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> MollyScalerOrm:
        raise NotImplementedError("MollyScalerEntity is not yet implemented")
