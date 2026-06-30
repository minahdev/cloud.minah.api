from __future__ import annotations

import logging
from dataclasses import dataclass, field

from star_craft.domain.ontology.communication.email_type import EmailType

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EmailSpec:
    """이메일 유형별 작성 규격 — 온톨로지가 정하는 '이렇게 써라'.

    점수·프롬프트 같은 실행 로직은 담지 않는다. 규격(지식)만 보관한다.
    """

    type_label: str  # 사람이 읽는 유형명 ("회의 안내")
    tone: str  # 말투 규격
    required_elements: tuple[str, ...] = field(default_factory=tuple)  # 본문 필수 요소


# 커뮤니케이션 온톨로지 — 유형 ↔ 작성 규격 (전역 지식, Hub 소유).
COMMUNICATION_TAXONOMY: dict[EmailType, EmailSpec] = {
    EmailType.GENERAL: EmailSpec("일반", "정중하고 간결한", ()),
    EmailType.NOTICE: EmailSpec("안내", "정중하고 명확한", ("핵심 안내 사항", "기한")),
    EmailType.MEETING: EmailSpec("회의 안내", "정중한", ("일시", "장소", "안건")),
    EmailType.APOLOGY: EmailSpec("사과", "진중하고 정중한", ("사과 대상", "원인", "재발 방지책")),
    EmailType.PROMOTION: EmailSpec("홍보", "활기차고 설득력 있는", ("핵심 혜택", "적용 기간", "행동 유도(CTA)")),
}


def get_email_spec(email_type: EmailType) -> EmailSpec:
    """유형에 맞는 작성 규격을 돌려준다. 미정의 유형은 GENERAL로 폴백."""
    matched = email_type in COMMUNICATION_TAXONOMY
    spec = COMMUNICATION_TAXONOMY.get(email_type, COMMUNICATION_TAXONOMY[EmailType.GENERAL])
    logger.info(
        "[2/3][온톨로지 통과] type=%s (%s) -> label=%s | tone=%s | 필수요소=%s",
        email_type.value,
        "정의됨" if matched else "미정의→GENERAL 폴백",
        spec.type_label,
        spec.tone,
        list(spec.required_elements),
    )
    return spec
