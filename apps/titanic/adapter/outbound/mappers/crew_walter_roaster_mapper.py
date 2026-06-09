from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.crew_walter_roaster_orm import WalterRoasterOrm


class WalterRoasterMapper:
    """WalterRoasterOrm(DB) ↔ WalterRoasterEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: WalterRoasterOrm) -> Any:
        raise NotImplementedError("WalterRoasterOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> WalterRoasterOrm:
        raise NotImplementedError("WalterRoasterEntity is not yet implemented")
