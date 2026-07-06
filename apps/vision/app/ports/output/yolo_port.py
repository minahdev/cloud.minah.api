from __future__ import annotations

from abc import ABC, abstractmethod


class YoloDatasetPort(ABC):
    """YOLO 데이터셋 공급 게이트웨이 (구현체는 로컬 디렉터리·S3 등).

    App(학습 로직)은 데이터가 어디서 오는지 몰라야 한다.
    구현체가 YOLO 분류 포맷(train/ · val/ · <클래스명>/ 이미지)을
    검증하고, ultralytics `data=` 인자로 넘길 **데이터셋 루트 경로**를 돌려준다.
    """

    @abstractmethod
    def get_dataset_root(self) -> str:
        """YOLO 학습에 넘길 데이터셋 루트 디렉터리의 절대 경로."""
        raise NotImplementedError
