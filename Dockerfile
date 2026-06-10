# 1. 파이썬 기반 이미지 가져오기
FROM python:3.13-slim

# 2. 도커 내부에 작업할 폴더 만들기
WORKDIR /app

# 3. 라이브러리 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 나머지 모든 소스코드 복사
COPY . .

# 5. FastAPI 서버 실행 (8000 포트)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
