from __future__ import annotations

from typing import Any

from silicon_valley.adapter.outbound.orm.piper_dinesh_dash_orm import DineshDashOrm


class DineshDashMapper:
    """DineshDashOrm(DB) ↔ DineshDashEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: DineshDashOrm) -> Any:
        raise NotImplementedError("DineshDashOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> DineshDashOrm:
        raise NotImplementedError("DineshDashEntity is not yet implemented")
