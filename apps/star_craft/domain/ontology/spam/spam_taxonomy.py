from __future__ import annotations

from dataclasses import dataclass, field

from star_craft.domain.ontology.spam.spam_category import SpamCategory


@dataclass(frozen=True)
class SpamConcept:
    """스팸 개념 하나 — 분류 + 그 개념을 가리키는 신호(키워드).

    온톨로지의 '노드'에 해당한다. 점수·임계값 같은 판정 로직은 담지 않는다.
    """

    category: SpamCategory
    keywords: tuple[str, ...] = field(default_factory=tuple)


# 스팸 온톨로지 — 개념 노드 목록 (전역 지식, Hub 소유).
SPAM_TAXONOMY: tuple[SpamConcept, ...] = (
    SpamConcept(
        category=SpamCategory.PHISHING,
        keywords=("비밀번호 확인", "계정 정지", "본인 인증", "보안 경고", "로그인 시도", "verify your account"),
    ),
    SpamConcept(
        category=SpamCategory.ADVERTISING,
        keywords=("할인", "무료 체험", "이벤트 당첨", "특가", "광고", "구독 신청"),
    ),
    SpamConcept(
        category=SpamCategory.IMPERSONATION,
        keywords=("국세청", "관세청", "택배 미수령", "대표이사", "긴급 송금 요청"),
    ),
)
