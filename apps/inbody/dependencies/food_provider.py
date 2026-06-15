from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from inbody.adapter.outbound.pg.food_pg_repository import FoodPgRepository
from inbody.app.ports.input.food_use_case import FoodUseCase
from inbody.app.use_cases.food_interactor import FoodInteractor


def get_food_use_case(
    db: AsyncSession = Depends(get_db),
) -> FoodUseCase:
    return FoodInteractor(repository=FoodPgRepository(db))
