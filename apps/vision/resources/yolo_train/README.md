# yolo_train — 얼굴 분류 데이터셋

YOLO **분류(classification)** 포맷. 이 폴더가 `LocalYoloDatasetAdapter`가 읽는 데이터셋 루트다.

```
yolo_train/
├── train/                # 학습셋
│   ├── ben_afflek/       # 클래스(인물)별 폴더
│   ├── elton_john/
│   ├── jerry_seinfeld/
│   ├── madonna/
│   └── mindy_kaling/
├── val/                  # 검증셋 (train과 동일한 클래스 폴더 구성)
│   └── ...
└── runs/                 # 학습 산출물(가중치·로그) — 실행 시 자동 생성
```

- **클래스 = 폴더 이름.** 인물을 추가하려면 `train/`·`val/` 양쪽에 같은 이름의 폴더를 만들고 이미지를 넣으면 된다.
- detection이 아니라 classification이라 bbox 라벨(`.txt`)·`data.yaml`은 **필요 없다.**
- 학습된 가중치: `runs/face_cls/weights/best.pt`

실행: 저장소 루트 `minahai/`에서 `python apps/vision/tests/yolo_demo.py`
