from __future__ import annotations

from enum import Enum


class SpamCategory(str, Enum):
    """스팸 메일의 상위 분류 개념.

    온톨로지 노드(개념)만 정의한다 — 판정 로직은 스포크(spam_filter)에 둔다.
    """

    HAM = "ham"  # 정상 메일
    PHISHING = "phishing"  # 피싱 (계정·금융 정보 탈취 유도)
    ADVERTISING = "advertising"  # 광고·홍보
    IMPERSONATION = "impersonation"  # 사칭 (기관·지인 위장)
