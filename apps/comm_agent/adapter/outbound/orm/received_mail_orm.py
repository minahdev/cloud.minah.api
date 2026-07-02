from datetime import datetime

from comm_agent.app.ports.output.embedding_port import EMBEDDING_DIM
from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.theone_base import Base


class ReceivedMailOrm(Base):
    """n8n(Gmail)에서 전달받아 저장한 수신 메일 1건."""

    __tablename__ = "received_mails"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender: Mapped[str] = mapped_column(String, nullable=False)  # 보낸 사람 (From)
    subject: Mapped[str] = mapped_column(String, nullable=False, default="")
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    # 메일 내용(subject+body) 임베딩. pgvector 의미 검색용.
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM), nullable=True)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
