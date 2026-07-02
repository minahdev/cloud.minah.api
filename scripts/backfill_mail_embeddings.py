"""received_mails 중 embedding이 비어있는(NULL) 과거 메일에 임베딩을 채운다.

기존 파이프라인(OllamaEmbeddingAdapter)을 그대로 재사용한다.
컨테이너 안에서 실행해야 pgvector/ollama 호스트가 해석된다.

사용법:
  docker exec minah_backend python scripts/backfill_mail_embeddings.py
"""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BACKEND_DIR / "apps"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(APPS_DIR))

load_dotenv(BACKEND_DIR / ".env")

from sqlalchemy import select

from comm_agent.adapter.outbound.embedding.ollama_embedding_adapter import OllamaEmbeddingAdapter
from comm_agent.adapter.outbound.orm.received_mail_orm import ReceivedMailOrm
from core.matrix.database_manager import get_async_session_factory


async def main() -> None:
    factory = get_async_session_factory()
    if factory is None:
        print("DATABASE_URL이 설정되지 않았습니다.")
        return

    embedder = OllamaEmbeddingAdapter()

    async with factory() as session:
        rows = (
            await session.execute(
                select(ReceivedMailOrm)
                .where(ReceivedMailOrm.embedding.is_(None))
                .order_by(ReceivedMailOrm.id)
            )
        ).scalars().all()

        total = len(rows)
        print(f"임베딩 없는 메일 {total}건 발견.")

        for i, row in enumerate(rows, start=1):
            content = f"{row.subject}\n\n{row.body}".strip()
            row.embedding = await embedder.embed(content)
            print(f"  [{i}/{total}] id={row.id} 채움 | {row.subject[:30]}")

        await session.commit()
        print(f"완료: {total}건 임베딩 저장.")


if __name__ == "__main__":
    asyncio.run(main())
