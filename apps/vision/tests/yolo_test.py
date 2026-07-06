"""YOLO Hello World — 사전학습 모델로 샘플 이미지를 탐지하고 결과 창을 띄운다."""

from pathlib import Path

from ultralytics import YOLO


def main() -> None:
    # 1. 사전학습된 YOLO 모델 로드 (없으면 자동 다운로드됨, ~6MB)
    model = YOLO("yolov8n.pt")

    # 2. 추론 실행 — ultralytics 기본 샘플 이미지(버스) 사용
    #    (인터넷에서 자동 다운로드됨. 로컬 이미지면 경로를 넣으면 됨)
    results = model("https://ultralytics.com/images/bus.jpg")

    # 3. 탐지 결과를 콘솔에 출력
    for r in results:
        print(f"탐지된 객체 수: {len(r.boxes)}")
        for box in r.boxes:
            cls_name = model.names[int(box.cls)]
            conf = float(box.conf)
            print(f"  - {cls_name} (신뢰도 {conf:.2f})")

    # 4. 바운딩박스가 그려진 결과를 이미지 파일로 저장
    #    (팝업 창 대신 파일로 저장 → VS코드에서 열어서 확인)
    out_path = Path(__file__).parent / "result.jpg"
    results[0].save(filename=str(out_path))
    print(f"\n결과 저장됨 → {out_path}")
    print("VS코드 탐색기에서 result.jpg 를 클릭하면 탐지 화면을 볼 수 있음.")


if __name__ == "__main__":
    main()
