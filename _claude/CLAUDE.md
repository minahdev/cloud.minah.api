# minahai — 백엔드 규칙

FastAPI 백엔드 전용 규칙. 전역 행동 원칙은 [루트 CLAUDE.md](../../CLAUDE.md) 참고.

---

## 1. 클린 아키텍처 + 헥사고날

### 1.1 의존 방향 (안쪽으로만)

```
[Inbound Adapter]  →  [Application]  →  [Outbound Port]
     HTTP/Router         Use Case           Repository ABC
     Pydantic Schema     Interactor              ↑
     CSV Parser          Command/DTO             │
                                      [Outbound Adapter] ──┘
                                           PG Repository
                                           ORM Model
```

- **도메인·유스케이스**는 FastAPI·SQLAlchemy·HTTP에 **의존하지 않는다**.
- **어댑터**만 프레임워크·DB를 안다.
- **의존성 조립(Composition Root)** 은 `dependencies/` 또는 `main.py` / `deps.py`에서만 한다.

### 1.2 레이어 역할

| 레이어 | 경로 패턴 | 책임 |
|--------|-----------|------|
| **Inbound API** | `adapter/inbound/api/v1/*_router.py` | HTTP만: 파라미터 수신, `Depends`, 응답 모델. **비즈니스 로직 금지** |
| **Inbound 보조** | `adapter/inbound/api/schemas/`, `*_csv_parser.py` | Pydantic 검증, CSV 파싱 — **무상태** 변환 |
| **Input Port** | `app/ports/input/*_use_case.py` | `ABC` + `@abstractmethod` — 유스케이스 계약 |
| **Application** | `app/use_cases/*_interactor.py` | 오케스트레이션, Command/DTO 조립, 로깅 |
| **Output Port** | `app/ports/output/*_repository.py` | 저장소 계약 (ABC) |
| **Outbound PG** | `adapter/outbound/pg/*_pg_repository.py` | Port 구현, SQLAlchemy 세션 사용 |
| **Outbound ORM** | `adapter/outbound/orm/*_orm.py` | 테이블 매핑 (`__tablename__`) |
| **DTO / Command** | `app/dtos/` | 유스케이스·레포 사이 데이터 (ORM과 분리) |
| **DI Factory** | `dependencies/*.py` | `get_db` → Repository → Interactor 조립 |

### 1.3 라우터는 얇게 (Thin Controller)

**좋은 예:**
- `UploadFile` 읽기 → CSV 파서로 파싱 → UseCase에 위임
- 구현체(`*PgRepository`)를 import하지 않음
- `Depends(get_*_use_case)` 로 **포트 타입**만 주입

**나쁜 예:**
- 라우터에서 `session.execute`, bcrypt, CSV 루프, commit
- Interactor 대신 Repository를 직접 호출

---

## 2. SOLID

### SRP — 단일 책임

| 클래스 | 책임 하나 |
|--------|-----------|
| `*Router` | HTTP 입출력 |
| `*Interactor` | Command 조립 + 저장 오케스트레이션 |
| `*PgRepository` | Postgres upsert/delete |
| `*_csv_parser` | 바이트/텍스트 → Schema 리스트 |
| `UserService` (secom) | 회원·로그인·프로필 유스케이스 |
| `CommunityController` (inbody) | HTTP 예외 매핑 + Service 위임 |

**한 파일에 "라우트 + SQL + 비즈니스 규칙"을 섞지 않는다.**

### DIP — 의존성 역전 (가장 중요)

1. 고수준(Interactor)은 **추상(Port)** 에만 의존.
2. 저수준(PG Repository)이 Port를 **구현**.
3. 조립은 `dependencies/` 팩토리에서만.

```python
# dependencies/foo.py — Composition Root
def get_foo_use_case(db: AsyncSession = Depends(get_db)) -> FooUseCase:
    repository: FooRepository = FooPgRepository(session=db)
    return FooInteractor(repository=repository)
```

**금지:** Router → `*PgRepository` 직접 import.

---

## 3. FastAPI 관례

### 진입점

- **단일 앱:** `minahai/main.py` — `lifespan`에서 `create_database_tables`, `include_router`.
- **titanic 집계:** `titanic/adapter/inbound/api/__init__.py` → `titanic_router`.

### 라우트 prefix

| 모듈 | prefix |
|------|--------|
| titanic 캐릭터 | `/titanic/<name>` |
| inbody | `/community/...`, `/notices`, ... |
| secom | **`main.py`에 직접** `/signup`, `/login`, `/mypage`, `/schedule/...` |

### 의존성 주입

```python
from minahai.core.matrix.oracle_database import get_db  # SSOT
```

| 제공자 | 위치 |
|--------|------|
| `get_db` | `minahai.core.matrix.oracle_database` |
| `inject_keymaker` | `apps/deps.py` |
| 도메인별 Use Case | `<app>/dependencies/*.py` |
| inbody Controller | `inbody/deps.py` |

### 스키마 vs DTO

| 종류 | 위치 | 용도 |
|------|------|------|
| **Pydantic Schema** | `adapter/inbound/api/schemas/` | HTTP 요청·응답, OpenAPI |
| **Command/DTO** | `app/dtos/` | 유스케이스·레포 내부 (프레임워크 무관) |

### Windows / Neon

- `main.py` · `oracle_database.py`: Windows에서 `WindowsSelectorEventLoopPolicy` (psycopg async).
- Neon: `pool_pre_ping=True`, `pool_recycle=1800`, URL에 `sslmode=require` 자동 보강.
- `DATABASE_URL` 없으면 `get_db` → HTTP 503.

---

## 4. 데이터베이스 · ERD

**SSOT:** `docs/DevOps/Backend/PACE_FULL_ERD.md`

### FK 허브

- 대부분의 사용자 데이터는 **`secom_users.id` (int PK)** 에 FK.
- 로그인 문자열은 **`secom_users.user_id` (varchar UK)**.

### id vs user_id (혼동 주의)

| 컬럼 | 의미 |
|------|------|
| `secom_users.id` | DB 내부 정수 PK — inbody FK가 가리키는 값 |
| `secom_users.user_id` | 로그인 ID 문자열 |
| `schedule_access_grants.user_id` | 로그인 **문자열** (DB FK 없음, 앱 로직 연결) |
| `schedule_invite_codes.created_by_user_id` | 코치 로그인 문자열 |

### 앱 ↔ 테이블 매핑

| 테이블 | 앱 |
|--------|-----|
| `secom_users`, `user_information`, `schedule_*` | secom |
| `community_posts`, `community_comments`, `community_post_cheers` | inbody |
| `today_stories`, `train_daily_logs`, `lessons`, `notices` | inbody |
| `titanic_person`, `titanic_booking` | titanic |

### ORM 등록

새 테이블 추가 시 `core/matrix/oracle_database.py`의 `_import_orm_models()`에 import 추가.

---

## 5. 앱별 아키텍처 성숙도

| 앱 | 패턴 | 비고 |
|----|------|------|
| **titanic** | 헥사고날 **표준** — Port / Interactor / DI / thin router | 새 백엔드 기능의 **참조 구현** |
| **secom** | 헥사고날 골격 + `UserService` Facade, API는 `main.py` | `ports/` 일부 stub |
| **inbody** | Router → Controller → Service → Repository (전통 3계층) | `secom.UserRepository`로 사용자 조회 |

- **새 secom 기능:** 가능하면 titanic식 Port+Interactor+`dependencies/`로 점진 이전.
- **새 inbody 기능:** 기존 Controller/Service/Repository 스타일 유지.
- **새 앱 추가:** titanic을 참조 구현으로 복제.

→ 새 기능 체크리스트: [minahai/apps/titanic/_docs/CLAUDE.md](../apps/titanic/_docs/CLAUDE.md)


# com.ragwatson

이 저장소는 Cursor·Claude 등 **LLM 코딩 보조**를 쓸 때, 모델이 흔히 빠지는 실패(묵시적 가정, 과잉 구현, 불필요하게 넓은 diff, 모호한 “완료”)를 줄이기 위한 **하네스 엔지니어링(harness engineering)** 을 코드와 함께 두는 레이아웃을 전제로 한다.

행동 지침의 의도는 안드레아 카파시가 널리 정리한 **네 가지 원칙**과 같다.

1. **구현 전 사고** — 가정을 말로 밝히고, 애매하면 질문·대안 제시.
2. **단순성 우선** — 요구를 만족하는 최소 코드, 추측 기능 금지.
3. **정밀한 수정** — 필요한 줄만, 스타일·무관 코드 존중.
4. **목표 중심 실행** — 검증 가능한 성공 기준과 루프.

> **트레이드오프:** 속도보다 신중함·검증 가능성. 사소한 편집은 맥락에 따라 완화해도 된다.

---

## 문서 맵 (하네스 층)

| 파일 | 역할 |
|------|------|
| [`CLAUDE.md`](CLAUDE.md) | 네 원칙의 **본문**(설명·예시·체크리스트). |
| [`.cursorrules`](../../.cursorrules) | Cursor에 항상 올라가는 **짧은 끈**. |
| [`CURSOR.md`](../../CURSOR.md) | Cursor **도구·워크플로**와 원칙을 맞추는 메모. |

경로별 세부 규칙이 있으면 `.cursor/rules/*.mdc`에 두고, 위 문서와 **병합**해서 해석한다.

---

## 쓰는 사람에게

- 작업을 맡길 때 **성공 기준**을 한 줄이라도 적는다(어떤 테스트가 통과하는지, 어떤 화면을 어떻게 확인하는지).
- “전부 개선”처럼 범위가 큰 요청은 **단계와 검증**을 나눈다.
- 비밀·키는 규칙 파일에 넣지 않는다.

에이전트·기여자는 위 문서를 읽은 뒤, 같은 루프(**목표 → 최소 변경 → 검증**)로 맞춘다.
