from __future__ import annotations

from abc import ABC, abstractmethod

from comm_agent.app.dtos.contact_dto import ContactCommand, ContactView


class ContactRepositoryPort(ABC):
    """주소록 저장·조회 게이트웨이."""

    @abstractmethod
    async def save_contacts(self, commands: list[ContactCommand]) -> int:
        pass

    @abstractmethod
    async def list_contacts(self) -> list[ContactView]:
        pass

    @abstractmethod
    async def search_contacts(self, keyword: str) -> list[ContactView]:
        pass
