# titanic — 앱 규칙

타이타닉 앱 전용 규칙. 백엔드 공통 규칙은 [minahai/CLAUDE.md](../../../CLAUDE.md) 참고.

---

## 1. 캐릭터 네이밍 패턴

각 승객/도메인 객체가 **독립적인 Use Case·Router·Repository 세트**를 가진다.

| 캐릭터 | 역할 예 |
|--------|---------|
| James (Director) | CSV 업로드, 전체 승객 저장 |
| Walter | 자기소개 로그 조회 |
| Rose | 모델 관련 유스케이스 |
| Smith (Captain) | 채팅, 자기소개 |

**새 캐릭터 추가 = 기존 파일 세트 복제 후 이름·도메인만 변경.**

---

## 2. 파일 구조 (캐릭터당)

```
titanic/
├── app/
│   ├── ports/
│   │   ├── input/<name>_use_case.py       # ABC
│   │   └── output/<name>_repository.py    # ABC
│   ├── dtos/<name>_dto.py                 # Command / Response
│   └── use_cases/<name>_interactor.py     # Port 구현
├── adapter/
│   ├── inbound/api/
│   │   ├── schemas/<name>_schema.py       # Pydantic
│   │   └── v1/<name>_router.py            # thin router
│   └── outbound/
│       ├── orm/<name>_orm.py              # ORM 모델 (필요 시)
│       └── pg/<name>_pg_repository.py    # Repository 구현
└── dependencies/<name>_provider.py       # DI 팩토리
```

---

## 3. 새 캐릭터 체크리스트

1. [ ] `app/ports/input/<name>_use_case.py` — ABC 정의
2. [ ] `app/ports/output/<name>_repository.py` — ABC 정의
3. [ ] `app/dtos/<name>_dto.py` — Command/Response
4. [ ] `app/use_cases/<name>_interactor.py` — Port 구현, Repository 생성자 주입
5. [ ] `adapter/outbound/orm/<name>_orm.py` — 테이블 모델 (필요 시)
6. [ ] `adapter/outbound/pg/<name>_pg_repository.py` — Repository Port 구현
7. [ ] `adapter/inbound/api/schemas/<name>_schema.py` — Pydantic
8. [ ] `adapter/inbound/api/v1/<name>_router.py` — thin router
9. [ ] `dependencies/<name>_provider.py` — DIP 팩토리
10. [ ] `adapter/inbound/api/__init__.py` — router 등록
11. [ ] `core/matrix/oracle_database.py` → `_import_orm_models()`에 ORM import 추가
12. [ ] 수동 검증: 서버 기동 → `/docs`에서 엔드포인트 확인

---

## 4. DB 패턴

- `titanic_person`: `passenger_id` (int) PK
- `titanic_booking`: `passenger_id` FK → person
- PG upsert: `INSERT ... ON CONFLICT DO UPDATE`
- booking: 해당 passenger 기존 행 DELETE 후 upsert

---

## 5. Import 경로 (titanic 내부)

```python
# ✅ titanic 내부에서
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer

# ❌ 금지
from minahai.apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
```


## 타이타닉 도메인 문서 연결 

* 타이타닉 도메인 문서 연결
* 타이타닉 피쳐 정리 : [[titanic-features]]
* 타이타닉 머신 러닝 : [[titanic-machine-learning]]
* 타이타닉 ERD : [[titanic-erd]]
* 타이타닉 NF : [[titanic-nf]]
* 타이타닉 알고리즘 : [[titanic-algorithm]]