# James FastAPI 초기화 상태 (Cursor Memory)

## 프로젝트 구조

```
apps/
└── titanic/
    └── app/
        ├── james.py       ← 메인 FastAPI 앱
        └── walter.py      ← Walter 모듈 (별도 관리)
```

---

## `apps/titanic/app/james.py` — 초기화 상태

```python
from fastapi import FastAPI, Query

from .walter import Walter

app = FastAPI(title="Titanic (James)")


class James:
    def __init__(self):
        pass


@app.get("/")
def read_root():
    return {"message": "FastAPI 초기화 성공", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("apps.titanic.app.james:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 초기화 상태 요약

| 항목 | 내용 |
|------|------|
| **앱 이름** | `Titanic (James)` |
| **프레임워크** | FastAPI |
| **진입점** | `apps.titanic.app.james:app` |
| **호스트** | `127.0.0.1` |
| **포트** | `8000` |
| **reload** | `True` |
| **등록된 라우트** | `GET /` → `{"message": "FastAPI 초기화 성공", "docs": "/docs"}` |
| **API 문서** | `http://127.0.0.1:8000/docs` |

---

## 의존성

- `fastapi`
- `uvicorn`
- `.walter` 모듈 (`Walter` 클래스)

---

## 실행 방법

```bash
# 직접 실행
python -m apps.titanic.app.james

# 또는 uvicorn으로 실행
uvicorn apps.titanic.app.james:app --host 127.0.0.1 --port 8000 --reload
```

---

## Cursor 규칙 (AI 참고용)

- `james.py`를 수정할 때 이 파일의 초기화 상태를 기준점으로 사용할 것
- `Walter` import는 반드시 유지할 것
- `FastAPI(title="Titanic (James)")` 타이틀은 변경하지 말 것
- 새 라우트 추가 시 `read_root()` 아래에 순서대로 추가할 것
- `James` 클래스는 현재 비어 있는 상태이며, 비즈니스 로직 확장 시 이 클래스를 활용할 것
