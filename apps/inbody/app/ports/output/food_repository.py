from __future__ import annotations

from abc import ABC, abstractmethod

from inbody.app.dtos.food_dto import FoodCreateCommand, FoodDto


class FoodRepository(ABC):

    @abstractmethod
    async def search_by_name(self, keyword: str) -> list[FoodDto]:
        pass

    @abstractmethod
    async def save(self, command: FoodCreateCommand) -> FoodDto:
        pass
