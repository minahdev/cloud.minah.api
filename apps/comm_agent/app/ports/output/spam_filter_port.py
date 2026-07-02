from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SpamVerdict:
    """메일 내용 필터 판정 결과."""

    is_normal: bool  # True면 정상 메일 (파이프라인 통과)
    label: str       # 모델이 예측한 라벨 (예: clean, 악플/욕설)
    score: float     # 신뢰도


class SpamFilterPort(ABC):
    """메일 내용의 정상/비정상(비속어·혐오·스팸) 판정 게이트웨이."""

    @abstractmethod
    async def classify(self, text: str) -> SpamVerdict:
        pass
