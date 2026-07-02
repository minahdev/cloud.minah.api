"""KcELECTRA 기반 한국어 욕설·혐오 필터 (기본 모델: smilegate-ai/kor_unsmile).

- 모델은 무거우므로 프로세스당 한 번만 로딩(lru_cache 싱글톤)한다.
- 추론(blocking)은 이벤트 루프를 막지 않도록 executor에서 실행한다.
- 모델명은 .env 의 SPAM_FILTER_MODEL 로 교체 가능.
"""

from __future__ import annotations

import asyncio
import logging
import os
from functools import lru_cache
from typing import Any

from comm_agent.app.ports.output.spam_filter_port import SpamFilterPort, SpamVerdict

logger = logging.getLogger(__name__)

_MODEL_NAME = os.getenv("SPAM_FILTER_MODEL", "smilegate-ai/kor_unsmile")
# 정상으로 취급할 라벨(소문자). 이 라벨이 최상위면 통과시킨다.
_NORMAL_LABELS = {
    s.strip().lower()
    for s in os.getenv("SPAM_NORMAL_LABELS", "clean,정상,normal").split(",")
    if s.strip()
}


@lru_cache(maxsize=1)
def _get_pipeline() -> Any:
    import torch
    from transformers import pipeline

    device = 0 if torch.cuda.is_available() else -1
    logger.info("[KorUnsmileFilter] 모델 로딩: %s (device=%s)", _MODEL_NAME, device)
    return pipeline(
        "text-classification",
        model=_MODEL_NAME,
        device=device,
        truncation=True,
        max_length=512,
    )


class KorUnsmileSpamFilter(SpamFilterPort):
    async def classify(self, text: str) -> SpamVerdict:
        clf = _get_pipeline()
        # blocking 추론을 별도 스레드에서 실행
        result = await asyncio.get_running_loop().run_in_executor(None, clf, text)
        top = result[0]  # {'label': ..., 'score': ...}
        label = str(top["label"])
        is_normal = label.lower() in _NORMAL_LABELS
        logger.info(
            "[KorUnsmileFilter] label=%s score=%.3f → %s",
            label,
            float(top["score"]),
            "정상" if is_normal else "차단",
        )
        return SpamVerdict(is_normal=is_normal, label=label, score=float(top["score"]))
