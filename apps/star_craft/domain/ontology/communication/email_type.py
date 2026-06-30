from __future__ import annotations

from enum import Enum


class EmailType(str, Enum):
    """이메일 작성 유형 개념.

    온톨로지 노드(개념)만 정의한다 — 실제 작성 로직은 스포크(comm_agent)에 둔다.
    """

    GENERAL = "general"  # 일반
    NOTICE = "notice"  # 안내
    MEETING = "meeting"  # 회의 안내
    APOLOGY = "apology"  # 사과
    PROMOTION = "promotion"  # 홍보
