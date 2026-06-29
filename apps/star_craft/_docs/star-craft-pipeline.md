# star_craft Hub — Graph DB · Vector DB 파이프라인 전략

## 1. 개요

`star_craft`는 스타 토폴로지의 **Hub**다.  
스포크(secom · inbody · titanic)의 컨텍스트를 교차 연결하고 전역 인덱스를 관리한다.  
이를 위해 두 가지 DB가 필요하다:

| DB 종류 | 용도 | 추천 이미지 |
|---------|------|-------------|
| **Graph DB** | 스포크 간 관계(엔티티 연결, 온톨로지) 저장 | `neo4j:5` |
| **Vector DB** | 임베딩 기반 의미 검색, RAG 컨텍스트 | `qdrant/qdrant` |

> 실제 사용 DB가 다르면 아래 어댑터 구현체만 교체한다. Port(ABC)는 유지.

---

## 2. 아키텍처 — 헥사고날 레이어 매핑

```
[inbound]
  API / WebSocket / MCP
        │
        ▼
[app.use_cases]          ← 오케스트레이션만, 비즈니스 로직 없음
        │
        ├──▶ [app.ports.output.graph_port.py]   (ABC)
        │           │
        │           ▼
        │    [adapter.outbound.graph.neo4j_adapter.py]   ← Neo4j 구현체
        │
        └──▶ [app.ports.output.vector_port.py]  (ABC)
                    │
                    ▼
             [adapter.outbound.vector.qdrant_adapter.py]  ← Qdrant 구현체
```

---

## 3. Docker Compose 구성

```yaml
# docker-compose.yml (프로젝트 루트)
services:
  neo4j:
    image: neo4j:5
    ports:
      - "7474:7474"   # 브라우저 UI
      - "7687:7687"   # Bolt 프로토콜
    environment:
      NEO4J_AUTH: neo4j/your_password
    volumes:
      - neo4j_data:/data

  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  neo4j_data:
  qdrant_data:
```

---

## 4. 환경변수 (.env)

```env
# Graph DB
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Vector DB
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

---

## 5. Port 정의 (ABC)

### graph_port.py
```python
# star_craft/app/ports/output/graph_port.py
from abc import ABC, abstractmethod

class GraphPort(ABC):
    @abstractmethod
    async def save_node(self, label: str, props: dict) -> str: ...

    @abstractmethod
    async def save_relation(self, from_id: str, to_id: str, rel_type: str) -> None: ...

    @abstractmethod
    async def query(self, cypher: str, params: dict) -> list[dict]: ...
```

### vector_port.py
```python
# star_craft/app/ports/output/vector_port.py
from abc import ABC, abstractmethod

class VectorPort(ABC):
    @abstractmethod
    async def upsert(self, collection: str, id: str, vector: list[float], payload: dict) -> None: ...

    @abstractmethod
    async def search(self, collection: str, vector: list[float], top_k: int) -> list[dict]: ...
```

---

## 6. 어댑터 구현 위치

```
star_craft/
└── adapter/
    └── outbound/
        ├── graph/
        │   ├── __init__.py
        │   └── neo4j_adapter.py       ← GraphPort 구현
        └── vector/
            ├── __init__.py
            └── qdrant_adapter.py      ← VectorPort 구현
```

---

## 7. 의존성 패키지

```txt
# requirements.txt 추가
neo4j==5.*          # Neo4j Python 드라이버
qdrant-client==1.*  # Qdrant Python 클라이언트
```

---

## 8. 파이프라인 흐름 (예시: 스포크 데이터 허브 인덱싱)

```
1. secom에서 신규 회원 생성
        │
        ▼
2. star_craft Use Case가 이벤트 수신
        │
        ├──▶ Neo4j: User 노드 저장 + spoke 관계 엣지 생성
        └──▶ Qdrant: 프로필 임베딩 저장 (의미 검색용)
```

---

## 9. 구현 순서

```
1. docker-compose.yml 작성 → docker compose up -d
2. .env 환경변수 등록
3. graph_port.py, vector_port.py (ABC) 작성
4. neo4j_adapter.py 구현 → 연결 테스트
5. qdrant_adapter.py 구현 → 연결 테스트
6. dependencies/__init__.py에 어댑터 DI 등록
7. use_case에서 Port 주입 후 파이프라인 연결
```
