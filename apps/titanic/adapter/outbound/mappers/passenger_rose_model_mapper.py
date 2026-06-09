from __future__ import annotations

from typing import TYPE_CHECKING, Any

from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm

if TYPE_CHECKING:
    pass  # RosePassenger entity not yet defined


class RoseModelMapper:
    """RoseModelOrm(DB) ↔ RosePassenger(Domain Entity) 변환.

    passenger_rose_model_entity.py 에 Passenger 엔티티가 구현되면
    to_entity / to_orm 을 완성한다.
    """

    @staticmethod
    def to_entity(orm: RoseModelOrm) -> Any:
        # TODO: passenger_rose_model_entity.py 에 Passenger 구현 후 활성화
        raise NotImplementedError("RosePassenger entity not yet implemented")

    @staticmethod
    def to_orm(entity: Any) -> RoseModelOrm:
        # TODO: passenger_rose_model_entity.py 에 Passenger 구현 후 활성화
        raise NotImplementedError("RosePassenger entity not yet implemented")
