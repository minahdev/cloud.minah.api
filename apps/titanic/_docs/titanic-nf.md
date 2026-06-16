# 🚢 Titanic Project: Database Design & Test Harness Guide

본 문서는 타이타닉 데이터셋(`titanic.csv`)을 데이터베이스에 적재할 때, 도메인 컨셉을 극대화하고 머신러닝 파이프라인과의 정렬을 위해 **미니 3NF(2개 테이블)** 구조로 분리하여 설계한 명세서 및 하네스(Harness) 검증 가이드입니다.

---

## 1. 데이터베이스 논리 모델 (Logical Data Model)

전체 데이터를 한 테이블에 밀어 넣는 대신, **순수 승객 정보(개인 존엄성)**와 **Caledon 가문이 통제하는 자본/티켓 정보(생존과 직결된 인프라)**를 명확히 분리합니다.

### 👤 [Passenger 테이블]
> **Jack, Rose 본인들의 고유한 인적 정보**를 담는 테이블입니다. `Sex` 대신 보다 현대적이고 정제된 표현인 `Gender`를 사용합니다.

| 컬럼명 (Column) | 타입 (Type) | 제약조건 (Constraint) | 설명 (Description) |
| :--- | :--- | :--- | :--- |
| **PassengerId** | INT | **PRIMARY KEY** | 승객 고유 식별 번호 |
| **Name** | VARCHAR(255) | NOT NULL | 승객 전체 이름 (예: `Jack Dawson`) |
| **Gender** | VARCHAR(10) | NOT NULL | 성별 (`male` 또는 `female`) |
| **Age** | FLOAT | NULLABLE | 나이 (소수점 포함 가능) |

### 🎟️ [TicketAssignment 테이블]
> **티켓 등급, 요금, 객실, 그리고 대망의 생존 여부**까지 자본 및 환경과 결합된 정보가 기록되는 테이블입니다. `CaledonValidation`이 집중적으로 검증할 영역입니다.

| 컬럼명 (Column) | 타입 (Type) | 제약조건 (Constraint) | 설명 (Description) |
| :--- | :--- | :--- | :--- |
| **TicketId** | INT | **PRIMARY KEY, AUTO_INC** | 티켓 매핑 고유 ID |
| **PassengerId** | INT | **FOREIGN KEY** (Refs Passenger) | 해당 티켓을 소유한 승객 ID |
| **Pclass** | INT | NOT NULL (1~3) | 티켓 등급 (1 = 1등석, 2 = 2등석, 3 = 3등석) |
| **TicketNumber**| VARCHAR(50) | NOT NULL | 티켓 번호 (알파벳+숫자 혼용) |
| **Fare** | FLOAT | NOT NULL (ge=0.0) | 탑승 요금 (칼레돈 검증 핵심 컬럼) |
| **Cabin** | VARCHAR(50) | NULLABLE | 객실 번호 |
| **Embarked** | VARCHAR(5) | NULLABLE | 승선항 (`C`, `Q`, `S`) |
| **Survived** | INT | NOT NULL (0 또는 1) | 생존 여부 (0 = 사망, 1 = 생존) |

---

## 2. DDL SQL (SQLite / PostgreSQL 호환)

```sql
-- 1. Passenger 테이블 생성
CREATE TABLE passengers (
    passenger_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age REAL
);

-- 2. TicketAssignment 테이블 생성
CREATE TABLE ticket_assignments (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_id INTEGER NOT NULL,
    pclass INTEGER NOT NULL CHECK (pclass BETWEEN 1 AND 3),
    ticket_number VARCHAR(50) NOT NULL,
    fare REAL NOT NULL CHECK (fare >= 0.0),
    cabin VARCHAR(50),
    embarked VARCHAR(5),
    survived INTEGER NOT NULL CHECK (survived IN (0, 1)),
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id) ON DELETE CASCADE
);