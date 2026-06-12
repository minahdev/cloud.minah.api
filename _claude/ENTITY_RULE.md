# Entity / 테이블 규칙

이 프로젝트의 **모든 테이블**은 동일한 기본 키 규칙을 따릅니다.

## 기본 원칙

| 항목 | 규칙 |
|------|------|
| 기본 키(PK) 컬럼명 | **`id`** (통일) |
| 타입 | **`int`** (정수) |
| 생성 방식 | DB **자동 증감** (PostgreSQL: `SERIAL` / `IDENTITY`, Alembic: `autoincrement=True`) |
| 용도 | 시스템 내부용 고유 번호 (비즈니스 식별자와 분리) |

- 로그인 아이디(`user_id`), 이메일 등 **업무 식별자**는 별도 컬럼으로 두고, PK `id`와 혼용하지 않습니다.
- 외래 키(FK)는 가능하면 참조 테이블의 **`id`** 를 가리킵니다 (`user_id` 문자열을 PK로 쓰지 않음).

---

## SQLModel 정의 (권장 템플릿)

`sqlmodel` 엔티티를 추가·수정할 때 아래 패턴을 그대로 사용합니다.

```python
from typing import Optional

from sqlmodel import Field, SQLModel


class ExampleTable(SQLModel, table=True):
    __tablename__ = "example_table"

    # 1. 시스템 내부용 자동 증감 고유 번호 (기본 키)
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},  # DB 컬럼명: id
    )

    # 이하 비즈니스 컬럼 …
```

### 필드 의미

- `default=None` — INSERT 시 DB가 시퀀스/IDENTITY로 값을 채움.
- `primary_key=True` — 단일 PK.
- `sa_column_kwargs={"name": "id"}` — ORM 속성명과 DB 컬럼명을 **`id`** 로 명시 (다른 이름으로 매핑하지 않음).

---

## SQLAlchemy 2.0 (`Mapped`) 동일 규칙

`apps/secom` 등 SQLAlchemy `declarative` 모델도 **동일한 DB 스키마**를 만족해야 합니다.

```python
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ExampleTable(Base):
    __tablename__ = "example_table"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        name="id",
    )
```

- Python 속성명: **`id`**
- DB 컬럼명: **`id`**
- `autoincrement=True` — 정수 PK 자동 증감.

### FK 예시 (회원 → 프로필)

```python
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class UserInformation(Base):
    __tablename__ = "user_information"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("secom_users.id", ondelete="CASCADE"),
        unique=True,  # 회원 1명당 1행
        index=True,
    )
    # … 프로필 컬럼
```

비즈니스 로그인 아이디는 `secom_users`에 `login_id`(또는 `userid`) 같은 **별도 UNIQUE 컬럼**으로 둡니다.

---

## Alembic 마이그레이션

새 테이블 생성 시 PK는 항상 아래 형태입니다.

```python
sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
# …
sa.PrimaryKeyConstraint("id"),
```

기존 테이블이 문자열 PK(`user_id` 등)를 쓰는 경우:

1. `id` 컬럼 추가 + 기존 데이터 backfill  
2. FK를 `id` 기준으로 재연결  
3. 구 PK 컬럼은 UNIQUE 비즈니스 컬럼으로 변경  
4. 애플리케이션·API는 단계적으로 `id` 기준 조회로 전환  

마이그레이션은 `backend/alembic/versions/` 에 추가하고 `alembic upgrade head` 로 적용합니다.

---

## 체크리스트 (PR 전)

- [ ] 모든 `table=True` / `__tablename__` 엔티티에 **`id: int` PK** 가 있는가?
- [ ] PK 컬럼명이 DB에서 **`id`** 인가? (`user_id`, `uuid` 등을 PK로 쓰지 않았는가?)
- [ ] FK가 참조 테이블의 **`id`** 를 가리키는가?
- [ ] Alembic revision에 `id` + `autoincrement` 가 반영되었는가?

---

## 현재 코드베이스 (`secom`)

| 테이블 | PK | 비즈니스 식별자 / FK |
|--------|-----|----------------------|
| `secom_users` | `id` (int) | `user_id` (varchar, UNIQUE) — 로그인 아이디 |
| `user_information` | `id` (int) | `user_id` (int, FK → `secom_users.id`, UNIQUE) |

마이그레이션: `backend/alembic/versions/20260521_entity_id_pk.py` (`alembic upgrade head`)
