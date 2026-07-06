from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vision.app.dtos.yolo_dto import (
        RecognizeYoloCommand,
        RecognizeYoloResult,
        TrainYoloCommand,
        TrainYoloResult,
    )


class TrainYoloUseCase(ABC):
    """YOLO 분류 모델 파인튜닝 오케스트레이터."""

    @abstractmethod
    def train(self, command: TrainYoloCommand) -> TrainYoloResult:
        raise NotImplementedError


class RecognizeYoloUseCase(ABC):
    """학습된 모델로 얼굴 이미지가 누구인지 판별한다."""

    @abstractmethod
    def recognize(self, command: RecognizeYoloCommand) -> RecognizeYoloResult:
        raise NotImplementedError
