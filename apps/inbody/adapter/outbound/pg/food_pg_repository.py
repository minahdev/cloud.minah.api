from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inbody.adapter.outbound.orm.food_orm import Food
from inbody.app.dtos.food_dto import FoodCreateCommand, FoodDto
from inbody.app.ports.output.food_repository import FoodRepository


def _to_dto(row: Food) -> FoodDto:
    return FoodDto(
        id=row.id,
        name=row.name,
        calories_kcal=row.calories_kcal,
        protein_g=row.protein_g,
        carbs_g=row.carbs_g,
        fat_g=row.fat_g,
        serving_size=row.serving_size,
        serving_unit=row.serving_unit,
        created_by=row.created_by,
    )


class FoodPgRepository(FoodRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def search_by_name(self, keyword: str) -> list[FoodDto]:
        stmt = (
            select(Food)
            .where(Food.name.ilike(f"%{keyword}%"))
            .order_by(Food.name)
            .limit(50)
        )
        result = await self._session.execute(stmt)
        return [_to_dto(r) for r in result.scalars().all()]

    async def save(self, command: FoodCreateCommand) -> FoodDto:
        row = Food(
            name=command.name,
            calories_kcal=command.calories_kcal,
            protein_g=command.protein_g,
            carbs_g=command.carbs_g,
            fat_g=command.fat_g,
            serving_size=command.serving_size,
            serving_unit=command.serving_unit,
            created_by=command.created_by,
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _to_dto(row)
