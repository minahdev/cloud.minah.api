from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.passenger_isidor_couple_orm import IsidorCoupleOrm


class IsidorCoupleMapper:
    """IsidorCoupleOrm(DB) ↔ IsidorCoupleEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: IsidorCoupleOrm) -> Any:
        raise NotImplementedError("IsidorCoupleOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> IsidorCoupleOrm:
        raise NotImplementedError("IsidorCoupleEntity is not yet implemented")
