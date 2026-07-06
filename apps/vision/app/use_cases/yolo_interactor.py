"""YOLOv11 Nano 얼굴 분류 학습·추론 유스케이스.

- 데이터셋 공급은 YoloDatasetPort(Outbound)에 위임 → 소스가 로컬이든 S3든 무관.
- ultralytics 종속성은 이 레이어 안에서만 다룬다 (무거운 import는 실행 시점에).
- 모델: yolo11n-cls.pt (YOLOv11 Nano의 분류 버전, 약 2.6M 파라미터 초경량).
"""

from __future__ import annotations

import logging

from vision.app.dtos.yolo_dto import (
    RecognizeYoloCommand,
    RecognizeYoloResult,
    TrainYoloCommand,
    TrainYoloResult,
)
from vision.app.ports.input.yolo_use_case import RecognizeYoloUseCase, TrainYoloUseCase
from vision.app.ports.output.yolo_port import YoloDatasetPort

logger = logging.getLogger(__name__)


class TrainYoloInteractor(TrainYoloUseCase):
    def __init__(self, dataset: YoloDatasetPort) -> None:
        # 의존성 주입 — Outbound 구현체(Resource Adapter)를 주입받는다.
        self._dataset = dataset

    def train(self, command: TrainYoloCommand) -> TrainYoloResult:
        from ultralytics import YOLO  # 무거운 import는 실행 시점에

        # 1. 아웃바운드 포트로 데이터셋 루트 확보 (소스가 바뀌어도 이 코드는 안 바뀜)
        dataset_root = self._dataset.get_dataset_root()

        # 2. YOLOv11 Nano 분류 모델 로드 (없으면 자동 다운로드, ~5MB)
        model = YOLO("yolo11n-cls.pt")

        # 3. 파인튜닝 실행
        logger.info("[TrainYolo] 학습 시작 | data=%s epochs=%s", dataset_root, command.epochs)
        model.train(
            data=dataset_root,
            epochs=command.epochs,
            batch=command.batch,
            imgsz=command.imgsz,
            device=command.device,
            project=command.project or None,
            name=command.name,
        )

        # 4. 학습 산출물(가중치 경로·클래스) 반환
        best = str(model.trainer.best)          # runs/<name>/weights/best.pt
        save_dir = str(model.trainer.save_dir)
        classes = list(model.names.values())
        logger.info("[TrainYolo] 학습 완료 | weights=%s", best)

        return TrainYoloResult(weights_path=best, save_dir=save_dir, classes=classes)


class RecognizeYoloInteractor(RecognizeYoloUseCase):
    def recognize(self, command: RecognizeYoloCommand) -> RecognizeYoloResult:
        from ultralytics import YOLO  # 무거운 import는 실행 시점에

        model = YOLO(command.weights_path)
        result = model(command.image_path)[0]

        probs = result.probs
        top1 = int(probs.top1)
        name = model.names[top1]
        confidence = float(probs.top1conf)
        top5 = [(model.names[int(i)], float(probs.data[int(i)])) for i in probs.top5]

        logger.info("[RecognizeYolo] %s → %s (%.2f%%)", command.image_path, name, confidence * 100)
        return RecognizeYoloResult(name=name, confidence=confidence, top5=top5)
