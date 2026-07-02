from __future__ import annotations

import logging
import os

import ollama
from comm_agent.app.ports.output.embedding_port import EMBEDDING_DIM, EmbeddingPort

logger = logging.getLogger(__name__)


def _ollama_host() -> str:
    """OLLAMA_URL(.../api/chat)에서 베이스 호스트만 뽑아낸다."""
    url = (os.getenv("OLLAMA_URL") or "http://host.docker.internal:11434").strip()
    return url.split("/api/")[0]


class OllamaEmbeddingAdapter(EmbeddingPort):
    """Ollama 임베딩 모델로 텍스트를 벡터로 변환한다."""

    def __init__(self) -> None:
        self._client = ollama.AsyncClient(host=_ollama_host())
        self._model = os.getenv("OLLAMA_EMBED_MODEL", "bge-m3")

    async def embed(self, text: str) -> list[float]:
        response = await self._client.embeddings(model=self._model, prompt=text)
        vector = list(response["embedding"])
        if len(vector) != EMBEDDING_DIM:
            raise RuntimeError(
                f"임베딩 차원 불일치: got={len(vector)} expected={EMBEDDING_DIM} "
                f"(model={self._model}). Vector 컬럼 차원과 모델을 맞추세요."
            )
        logger.info("[OllamaEmbedding] 임베딩 생성 | dim=%s model=%s", len(vector), self._model)
        return vector
