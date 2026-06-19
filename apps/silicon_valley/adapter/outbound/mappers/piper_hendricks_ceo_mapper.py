from __future__ import annotations

from typing import Any

from silicon_valley.adapter.outbound.orm.piper_hendricks_ceo_orm import HendricksCeoOrm


class HendricksCeoMapper:
    """HendricksCeoOrm(DB) ↔ HendricksCeoEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: HendricksCeoOrm) -> Any:
        raise NotImplementedError("HendricksCeoOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> HendricksCeoOrm:
        raise NotImplementedError("HendricksCeoEntity is not yet implemented")
