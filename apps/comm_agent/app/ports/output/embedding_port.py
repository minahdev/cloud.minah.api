from __future__ import annotations

from abc import ABC, abstractmethod

# 임베딩 벡터 차원 (bge-m3 기준). 컬럼(Vector)과 반드시 일치해야 한다.
EMBEDDING_DIM = 1024


class EmbeddingPort(ABC):
    """텍스트를 임베딩 벡터로 변환하는 게이트웨이."""

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass
