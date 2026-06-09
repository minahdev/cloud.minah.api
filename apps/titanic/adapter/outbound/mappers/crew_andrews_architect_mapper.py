from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.crew_andrews_architect_orm import AndrewsArchitectOrm


class AndrewsArchitectMapper:
    """AndrewsArchitectOrm(DB) ↔ AndrewsArchitectEntity(Domain) 변환.

    ORM 테이블 컬럼과 Entity 필드가 정의되면 to_entity / to_orm 을 완성한다.
    """

    @staticmethod
    def to_entity(orm: AndrewsArchitectOrm) -> Any:
        raise NotImplementedError("AndrewsArchitectOrm is abstract — define __tablename__ and columns first")

    @staticmethod
    def to_orm(entity: Any) -> AndrewsArchitectOrm:
        raise NotImplementedError("AndrewsArchitectEntity is not yet implemented")
