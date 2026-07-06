"""YOLOv11 Nano 얼굴 분류 파이프라인 드라이버 (조립 + 실행).

헥사고날의 Inbound/Driver 역할:
  Outbound(데이터셋 어댑터) → App(학습·추론 유스케이스) 를 조립해 실행한다.

실행:
    cd minahai
    python apps/vision/tests/yolo_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# 단독 실행 시 `vision.` 패키지를 찾을 수 있게 apps 디렉터리를 경로에 추가
APPS_DIR = Path(__file__).resolve().parents[2]  # .../minahai/apps
sys.path.insert(0, str(APPS_DIR))

from vision.adapter.outbound.resource_adapters.yolo.yolo_dataset_adapter import (  # noqa: E402
    LocalYoloDatasetAdapter,
)
from vision.app.dtos.yolo_dto import RecognizeYoloCommand, TrainYoloCommand  # noqa: E402
from vision.app.use_cases.yolo_interactor import (  # noqa: E402
    RecognizeYoloInteractor,
    TrainYoloInteractor,
)

DATASET_DIR = Path(__file__).resolve().parents[1] / "resources" / "yolo_train"


def main() -> None:
    # 1. 인프라(Outbound) 초기화 — 데이터셋 소스 주입
    dataset = LocalYoloDatasetAdapter(base_path=str(DATASET_DIR))

    # 2. 학습(App) — 데이터셋 포트 주입 후 파인튜닝
    trainer = TrainYoloInteractor(dataset=dataset)
    print("[학습] YOLOv11 Nano 얼굴 분류 파인튜닝 시작...")
    trained = trainer.train(
        TrainYoloCommand(
            epochs=10,
            batch=16,
            imgsz=224,
            device="cpu",  # GPU 있으면 "0", 맥북이면 "mps"
            project=str(DATASET_DIR / "runs"),
            name="yolo11n_face",
        )
    )
    print(f"[완료] 학습 완료 | classes={trained.classes}")
    print(f"   가중치: {trained.weights_path}")

    # 3. 추론(App) — val/ 에서 이미지 1장 골라 인물 판별
    sample = next((DATASET_DIR / "val").rglob("*.jpg"))
    recognizer = RecognizeYoloInteractor()
    pred = recognizer.recognize(
        RecognizeYoloCommand(image_path=str(sample), weights_path=trained.weights_path)
    )
    print(f"\n[추론] 테스트 이미지: {sample.parent.name}/{sample.name}")
    print(f"   예측: {pred.name} ({pred.confidence:.2%})")
    print("   상위 후보:")
    for cls_name, prob in pred.top5:
        print(f"     - {cls_name}: {prob:.2%}")


if __name__ == "__main__":
    main()
