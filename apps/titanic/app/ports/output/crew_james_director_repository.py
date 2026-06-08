from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.crew_james_director_dto import BookingCommand, PersonCommand
from titanic.app.dtos.crew_james_director_dto import JamesDirectorResponse, JamesDirectorQuery


class JamesDirectorRepository(ABC):
    """James — CSV 업로드(승객 bulk 저장)."""

    @abstractmethod
    async def upload_titanic_file(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        pass


    @abstractmethod
    async def introduce_myself(self, query: JamesDirectorQuery) -> JamesDirectorResponse:
        pass