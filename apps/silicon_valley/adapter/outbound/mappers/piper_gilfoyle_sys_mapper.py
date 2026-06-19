from __future__ import annotations

from typing import Any

from silicon_valley.adapter.outbound.orm.piper_gilfoyle_sys_orm import GilfoyleSysOrm


class GilfoyleSysMapper:
    """GilfoyleSysOrm(DB) ↔ GilfoyleSysEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: GilfoyleSysOrm) -> Any:
        raise NotImplementedError("GilfoyleSysOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> GilfoyleSysOrm:
        raise NotImplementedError("GilfoyleSysEntity is not yet implemented")
