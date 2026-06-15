from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.food_dto import FoodCreateCommand, FoodDto, FoodSearchQuery


class FoodUseCase(ABC):

    @abstractmethod
    async def search(self, query: FoodSearchQuery) -> list[FoodDto]:
        pass

    @abstractmethod
    async def create(self, command: FoodCreateCommand) -> FoodDto:
        pass
