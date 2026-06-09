from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.crew_hartley_violin_orm import HartleyViolinOrm


class HartleyViolinMapper:
    """HartleyViolinOrm(DB) ↔ HartleyViolinEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: HartleyViolinOrm) -> Any:
        raise NotImplementedError("HartleyViolinOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> HartleyViolinOrm:
        raise NotImplementedError("HartleyViolinEntity is not yet implemented")
