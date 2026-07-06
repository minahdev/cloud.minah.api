# 1. 파이썬 기반 이미지 가져오기
FROM python:3.13-slim

# 2. 도커 내부에 작업할 폴더 만들기
WORKDIR /app

# 3. 시스템 라이브러리 설치 (LightGBM 의존성)
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

# 4. 라이브러리 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4-1. OpenCV/ultralytics 런타임 시스템 라이브러리 (slim 이미지에 없음)
#      pip 레이어 뒤에 둬서 torch 등 재설치 캐시를 깨지 않는다.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# 4. 나머지 모든 소스코드 복사
COPY . .

# 5. FastAPI 서버 실행 (8000 포트)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
