"""로컬 YOLO 분류 데이터셋 어댑터.

`resources/yolo_train/` 아래의 로컬 디렉터리를 데이터셋 소스로 사용한다.
나중에 S3에서 받아 쓰려면 이 파일 대신 `S3DatasetAdapter`만 새로 만들어
갈아 끼우면 되고, App(학습 로직)은 한 줄도 안 고친다.
"""

from __future__ import annotations

import logging
from pathlib import Path

from vision.app.ports.output.yolo_port import YoloDatasetPort

logger = logging.getLogger(__name__)


class LocalYoloDatasetAdapter(YoloDatasetPort):
    def __init__(self, base_path: str) -> None:
        self._base = Path(base_path)

    def get_dataset_root(self) -> str:
        # YOLO 분류 포맷은 루트 아래에 train/ 과 val/ 이 있어야 한다.
        for split in ("train", "val"):
            split_dir = self._base / split
            if not split_dir.is_dir():
                raise FileNotFoundError(
                    f"YOLO 분류 데이터셋에 '{split}/' 폴더가 없습니다: {split_dir}"
                )

        classes = sorted(p.name for p in (self._base / "train").iterdir() if p.is_dir())
        if not classes:
            raise FileNotFoundError(f"train/ 아래에 클래스 폴더가 없습니다: {self._base / 'train'}")

        logger.info("[LocalYoloDataset] root=%s classes=%s", self._base, classes)
        return str(self._base.resolve())
