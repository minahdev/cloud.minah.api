from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.passenger_ruth_validation_orm import RuthValidationOrm


class RuthValidationMapper:
    """RuthValidationOrm(DB) ↔ RuthValidationEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: RuthValidationOrm) -> Any:
        raise NotImplementedError("RuthValidationOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> RuthValidationOrm:
        raise NotImplementedError("RuthValidationEntity is not yet implemented")
