from __future__ import annotations

from inbody.app.dtos.food_dto import FoodCreateCommand, FoodDto, FoodSearchQuery
from inbody.app.ports.input.food_use_case import FoodUseCase
from inbody.app.ports.output.food_repository import FoodRepository


class FoodInteractor(FoodUseCase):

    def __init__(self, repository: FoodRepository) -> None:
        self._repository = repository

    async def search(self, query: FoodSearchQuery) -> list[FoodDto]:
        return await self._repository.search_by_name(query.keyword.strip())

    async def create(self, command: FoodCreateCommand) -> FoodDto:
        return await self._repository.save(command)
