from __future__ import annotations

from abc import ABC, abstractmethod


class OntologyGraphPort(ABC):
    """온톨로지를 그래프 저장소(Neo4j)에 적재하는 게이트웨이."""

    @abstractmethod
    async def sync_ontology(self, spam: list[dict], communication: list[dict]) -> dict:
        pass
