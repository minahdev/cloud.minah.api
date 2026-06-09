from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.crew_james_director_orm import JamesDirectorOrm


class JamesDirectorMapper:
    """JamesDirectorOrm(DB) ↔ JamesDirectorEntity(Domain) 변환."""

    @staticmethod
    def to_entity(orm: JamesDirectorOrm) -> Any:
        raise NotImplementedError("JamesDirectorOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> JamesDirectorOrm:
        raise NotImplementedError("JamesDirectorEntity is not yet implemented")
