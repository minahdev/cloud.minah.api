# Project - API Specification & Context

이 문서는 프로젝트  초기 설정 및 기술 스택을 정의합니다. 커서(Cursor) AI는 이 가이드를 바탕으로 코드를 생성하고 유지보수해야 합니다.

## 1. 프로젝트 개요
- **프레임워크**: FastAPI
- **엔트리포인트**: `james.py`
- **목적**: 데이터 처리 및 분석 서비스 제공

## 2. 기술 스택 및 환경
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Server**: Uvicorn (Host: 127.0.0.1, Port: 8000)
- **Core Modules**: 
    - `Walter`: 데이터 처리 및 로직 담당 클래스
    - `James`: 메인 로직 래퍼 클래스

## 3. 코드 아키텍처 규칙
- **FastAPI 초기화**: `app = FastAPI(title="Titanic (James)")` 형식을 유지할 것.
- **실행 방식**: `uvicorn.run("james:app", ...)`를 통해 실행되므로 파일 이름은 반드시 `james.py`여야 함.
- **모듈화**: 비즈니스 로직은 `James` 클래스 내부에 정의하거나 `Walter` 모듈을 활용할 것.

## 4. API 엔드포인트 기본값
- **Root (/)**: API 상태 확인 및 문서 경로(`docs`) 반환.
- **Swagger UI**: `/docs`에서 확인 가능.

## 5. 개발 가이드라인
- 새로운 엔드포인트를 생성할 때는 `app` 인스턴스를 사용하세요.
- 모든 비즈니스 로직은 타입 힌트(Type Hinting)를 엄격히 적용하세요.
- 에러 처리는 FastAPI의 `HTTPException`을 활용하세요.

---
*Last Updated: 2026-05-07*