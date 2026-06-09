from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.passenger_cal_tester_orm import CalTesterOrm


class CalTesterMapper:
    """CalTesterOrm(DB) ↔ CalTesterEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: CalTesterOrm) -> Any:
        raise NotImplementedError("CalTesterOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> CalTesterOrm:
        raise NotImplementedError("CalTesterEntity is not yet implemented")
