# minahai — 백엔드 규칙

FastAPI 백엔드 전용 규칙. 전역 행동 원칙은 [루트 CLAUDE.md](../../CLAUDE.md) 참고.

---

## 0. 프로젝트 정체성

사용자의 감정·상태·훈련 기록을 AI가 분석해 맞춤형 운동 루틴을 추천하는 퍼스널 트레이닝 플랫폼.

- **secom**: 회원가입·로그인·마이페이지·스케줄 접근 관리
- **inbody**: 커뮤니티·오늘의 이야기·훈련일지·공지·식단
- **titanic**: 헥사고날 아키텍처 참조 구현 (학습용 승객 도메인)

단일 진입점: `minahai/main.py` → FastAPI `lifespan`에서 DB 초기화 + 라우터 등록.

---

## 1. 클린 아키텍처 + 헥사고날

### 의존 방향 (안쪽으로만)

```
[Inbound Adapter]  →  [Application]  →  [Outbound Port]
  HTTP Router          Use Case           Repository ABC
  Pydantic Schema      Interactor              ↑
  CSV Parser           Command/DTO             │
                                    [Outbound Adapter] ──┘
                                      PgRepository / ORM
```

- **도메인·유스케이스**는 FastAPI·SQLAlchemy·HTTP에 의존하지 않는다.
- **어댑터**만 프레임워크·DB를 안다.
- **Composition Root**: `dependencies/*.py` 또는 `deps.py`에서만 조립.

### 레이어 역할

| 레이어 | 경로 패턴 | 책임 |
|--------|-----------|------|
| Inbound API | `adapter/inbound/api/v1/*_router.py` | HTTP 수신·응답만. 비즈니스 로직 금지 |
| Pydantic Schema | `adapter/inbound/api/schemas/` | HTTP 요청·응답, OpenAPI |
| Input Port | `app/ports/input/*_use_case.py` | ABC + @abstractmethod |
| Application | `app/use_cases/*_interactor.py` | Command 조립, 저장 오케스트레이션 |
| Output Port | `app/ports/output/*_port.py` | 저장소 계약 (ABC) |
| Outbound PG | `adapter/outbound/pg/*_repository.py` | Port 구현, SQLAlchemy 세션 |
| ORM | `adapter/outbound/orm/*_orm.py` | 테이블 매핑 (`__tablename__`) |
| Command/DTO | `app/dtos/` | 유스케이스·레포 내부 데이터 (프레임워크 무관) |
| DI Factory | `dependencies/*.py` | get_db → Repository → Interactor 조립 |

### DIP 패턴 (가장 중요)

```python
# dependencies/foo.py — Composition Root
def get_foo_use_case(db: AsyncSession = Depends(get_db)) -> FooUseCase:
    repository: FooRepository = FooPgRepository(session=db)
    return FooInteractor(repository=repository)
```

**금지:** Router → `*PgRepository` 직접 import.

---

## 2. 앱별 아키텍처 성숙도

| 앱 | 패턴 | 비고 |
|----|------|------|
| **titanic** | 헥사고날 **표준** — Port/Interactor/DI/thin router | 새 기능의 **참조 구현** |
| **secom** | 헥사고날 골격 + `UserService` Facade, API는 `main.py` | `ports/` 일부 stub |
| **inbody** | Router → Controller → Service → Repository (전통 3계층) | `secom.UserRepository`로 사용자 조회 |

- **새 secom 기능:** titanic식 Port+Interactor+`dependencies/`로 점진 이전.
- **새 inbody 기능:** 기존 Controller/Service/Repository 스타일 유지.
- **새 앱 추가:** titanic을 참조 구현으로 복제.

---

## 3. FastAPI 관례

### 진입점 & 라우터 등록

`minahai/main.py`:

```python
app.include_router(inbody_router)
app.include_router(titanic_router, prefix="/api")
# secom 라우트는 main.py에 직접 정의
```

### 라우트 prefix

| 모듈 | prefix 예 |
|------|-----------|
| secom | `/signup`, `/login`, `/mypage`, `/schedule/...` |
| inbody | `/community/...`, `/notices`, `/train/...` |
| titanic | `/api/titanic/<character>/...` |

### 의존성 주입 SSOT

```python
from minahai.core.matrix.oracle_database import get_db  # 항상 이 경로
```

| 제공자 | 위치 |
|--------|------|
| `get_db` | `minahai.core.matrix.oracle_database` |
| `inject_keymaker` | `apps/deps.py` |
| 도메인별 Use Case | `<app>/dependencies/*.py` |

### Windows / Neon

- `main.py`: `asyncio.WindowsSelectorEventLoopPolicy()` (psycopg async 필수)
- Neon: `pool_pre_ping=True`, `pool_recycle=1800`, URL `sslmode=require` 자동 보강
- `DATABASE_URL` 없으면 `get_db` → HTTP 503

---

## 4. 데이터베이스 · ERD

**SSOT:** `docs/DevOps/Backend/PACE_FULL_ERD.md`

### FK 허브

- 대부분 사용자 데이터: **`secom_users.id` (int PK)** 에 FK
- 로그인 문자열: **`secom_users.user_id` (varchar UK)**

### id vs user_id (혼동 주의)

| 컬럼 | 의미 |
|------|------|
| `secom_users.id` | DB 내부 정수 PK — inbody FK가 가리키는 값 |
| `secom_users.user_id` | 로그인 ID 문자열 |
| `schedule_access_grants.user_id` | 로그인 문자열 (DB FK 없음, 앱 로직 연결) |
| `schedule_invite_codes.created_by_user_id` | 코치 로그인 문자열 |

### 앱 ↔ 테이블 매핑

| 앱 | 테이블 |
|----|--------|
| secom | `secom_users`, `user_information`, `schedule_access_grants`, `schedule_invite_codes` |
| inbody | `community_posts`, `community_comments`, `community_post_cheers`, `today_stories`, `train_daily_logs`, `lessons`, `notices` |
| titanic | `titanic_person`, `titanic_booking` |

### ORM 등록

새 테이블 추가 시 `core/matrix/oracle_database.py`의 `_import_orm_models()`에 import 추가.

---

## 4-1. Entity / 테이블 규칙

이 프로젝트의 **모든 테이블**은 동일한 기본 키 규칙을 따릅니다.

### 기본 원칙

| 항목 | 규칙 |
|------|------|
| 기본 키(PK) 컬럼명 | **`id`** (통일) |
| 타입 | **`int`** (정수) |
| 생성 방식 | DB **자동 증감** (PostgreSQL: `SERIAL` / `IDENTITY`, Alembic: `autoincrement=True`) |
| 용도 | 시스템 내부용 고유 번호 (비즈니스 식별자와 분리) |

- 로그인 아이디(`user_id`), 이메일 등 **업무 식별자**는 별도 컬럼으로 두고, PK `id`와 혼용하지 않습니다.
- 외래 키(FK)는 가능하면 참조 테이블의 **`id`** 를 가리킵니다 (`user_id` 문자열을 PK로 쓰지 않음).

### SQLModel 정의 (권장 템플릿)

```python
from typing import Optional
from sqlmodel import Field, SQLModel


class ExampleTable(SQLModel, table=True):
    __tablename__ = "example_table"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    # 이하 비즈니스 컬럼 …
```

### SQLAlchemy 2.0 (`Mapped`) 동일 규칙

```python
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class ExampleTable(Base):
    __tablename__ = "example_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, name="id")
```

**FK 예시 (회원 → 프로필)**

```python
class UserInformation(Base):
    __tablename__ = "user_information"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("secom_users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
```

### Alembic 마이그레이션

```python
sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
sa.PrimaryKeyConstraint("id"),
```

### 체크리스트 (PR 전)

- [ ] 모든 `table=True` 엔티티에 **`id: int` PK** 가 있는가?
- [ ] PK 컬럼명이 DB에서 **`id`** 인가?
- [ ] FK가 참조 테이블의 **`id`** 를 가리키는가?
- [ ] Alembic revision에 `id` + `autoincrement` 가 반영되었는가?

---

## 5. titanic — 캐릭터 네이밍 & 헥사고날 참조

상세 규칙: [titanic/_docs/CLAUDE.md](../../minahai/apps/titanic/_docs/CLAUDE.md)

캐릭터별로 독립적인 Use Case·Router·Repository 세트 보유.

| 캐릭터 | 역할 |
|--------|------|
| James (Director) | CSV 업로드, 전체 승객 저장 |
| Walter (Roaster) | 자기소개 로그 조회 |
| Smith (Captain) | 채팅, 자기소개 |
| Rose (Model) | 모델 관련 유스케이스 |
| Jack (Trainer) | 훈련 관련 유스케이스 |

**새 캐릭터 = 기존 파일 세트 복제 후 이름·도메인만 변경.**

### 파일 구조 (캐릭터당)

```
titanic/
├── app/
│   ├── ports/input/<name>_use_case.py
│   ├── ports/output/<name>_port.py
│   ├── dtos/<name>_dto.py
│   └── use_cases/<name>_interactor.py
├── adapter/
│   ├── inbound/api/schemas/<name>_schema.py
│   ├── inbound/api/v1/<name>_router.py
│   └── outbound/
│       ├── orm/<name>_orm.py
│       └── pg/<name>_repository.py
└── dependencies/<name>_provider.py
```

### 새 캐릭터 체크리스트

1. `app/ports/input/<name>_use_case.py` — ABC
2. `app/ports/output/<name>_port.py` — ABC
3. `app/dtos/<name>_dto.py` — Command/Response
4. `app/use_cases/<name>_interactor.py` — Repository 생성자 주입
5. `adapter/outbound/orm/<name>_orm.py` — 테이블 모델
6. `adapter/outbound/pg/<name>_repository.py` — Port 구현
7. `adapter/inbound/api/schemas/<name>_schema.py` — Pydantic
8. `adapter/inbound/api/v1/<name>_router.py` — thin router
9. `dependencies/<name>_provider.py` — DIP 팩토리
10. `adapter/inbound/api/__init__.py` — router 등록
11. `core/matrix/oracle_database.py` → `_import_orm_models()` ORM import 추가
12. 수동 검증: 서버 기동 → `/docs` 엔드포인트 확인

---

## 6. Import 경로 규칙

#### Apps layer

```python
# ✅
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from inbody.app.use_cases.community_post_interactor import CommunityPostInteractor

# ❌ minahai 접두사 + apps 세그먼트 금지
from minahai.apps.titanic.app.ports.input... import ...
```

#### Core layer

```python
# ✅
from minahai.core.matrix.oracle_database import get_db

# ❌
from core.matrix.oracle_database import get_db
```

---

## 7. 금지 사항

- 라우터에 SQL·트랜잭션·비즈니스 로직 삽입
- `get_db` 임의 위치 중복 정의 — oracle_database SSOT
- Router → `*PgRepository` 직접 import
- 요청 범위 밖 리팩터링·관련 없는 앱 수정
- git commit/push — 사용자 명시 요청 시에만

---

## 8. 데이터 척도 원칙

### Categorical (범주형)

데이터가 카테고리로 묶일 때 사용한다.

| 척도 | 설명 | 예시 |
|------|------|------|
| **nominal** | 이름 기반, 순서 없음 | 청팀, 홍팀, 백팀 |
| **ordinal** | 순서(서열) 있음 | 1.매우낮음 2.낮음 3.보통 4.높음 5.매우높음 |

### Quantitative (수치형)

숫자로 셀 수 있을 때 사용한다.

| 척도 | 설명 | 예시 |
|------|------|------|
| **interval** | 기준점 없이 일정 구간 측정 | 온도, pH, 시간대 (10배 덥다 불가) |
| **ratio** | 절대 원점 기준, 비율 가능 | 나이, 돈, 몸무게 (10배 많다 가능) |

---

## 9. async def vs def 선택 원칙

| 성격 | 예시 | 형태 |
|------|------|------|
| **I/O-bound** — DB, 외부 API, LLM, 파일 I/O | `introduce_myself`, `chat` | `async def` |
| **CPU-bound** — 순수 연산, 형태소 분석(Kiwi), 수치 처리 | `analyze_intent` | `def` |

- `async def`는 코루틴을 만들 뿐, CPU 연산을 비블로킹으로 바꾸지 않는다.
- CPU-bound 메소드에 `async`를 붙이면 이벤트 루프를 막으면서 비블로킹처럼 보이는 거짓 표시가 된다.
- Kiwi 등 CPU 작업이 실제로 이벤트 루프 블로킹 문제가 된다면, 메소드를 `async`로 바꾸는 대신 호출 측에서 스레드풀로 넘긴다:

```python
result = await asyncio.to_thread(use_case.analyze_intent, question)
```
