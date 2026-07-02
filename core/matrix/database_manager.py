"""
Neon(Postgres) async SQLAlchemy 설정 (Single Source of Truth).

- 실행 진입점이 `backend/apps` 기준인 경우가 많아, 실제 import는
  `backend/apps/database.py` shim을 통해 이 모듈을 사용합니다.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
import selectors

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

_BACKEND_DIR = Path(__file__).resolve().parents[2]  # backend/
_ENV_PATH = _BACKEND_DIR / ".env"
load_dotenv(_ENV_PATH)

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()

# Ensure `backend/apps` packages (secom, inbody, titanic, ...) are importable
_APPS_DIR = _BACKEND_DIR / "apps"
if _APPS_DIR.exists() and str(_APPS_DIR) not in sys.path:
    sys.path.insert(0, str(_APPS_DIR))

if sys.platform == "win32":
    # psycopg async 호환을 위해 SelectorEventLoop 사용
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Base(DeclarativeBase):
    pass


engine = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


def _ensure_sslmode(url: str) -> str:
    """
    Neon(Postgres) 연결에서 SSL이 필수인 경우가 많다.
    .env를 읽지 않아도 안전하게 `sslmode=require`가 없으면 보강한다.
    """
    text = (url or "").strip()
    if not text:
        return text
    if "sslmode=" in text:
        return text
    joiner = "&" if "?" in text else "?"
    return f"{text}{joiner}sslmode=require"


def get_async_session_factory() -> async_sessionmaker[AsyncSession] | None:
    global engine, AsyncSessionLocal
    if not DATABASE_URL:
        return None
    if AsyncSessionLocal is None:
        engine = create_async_engine(
            _ensure_sslmode(DATABASE_URL),
            echo=False,
            pool_pre_ping=True,  # stale connection 자동 감지
            pool_recycle=1800,  # 주기적으로 커넥션 재생성 (Neon idle 종료 대응)
            pool_timeout=30,
        )
        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return AsyncSessionLocal


async def get_db():
    """FastAPI DI: 요청마다 AsyncSession을 열고 닫는다."""
    factory = get_async_session_factory()
    if factory is None:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL is not set or empty. Configure it to use the database.",
        )
    async with factory() as session:
        yield session


def _import_orm_models() -> None:
    """Base.metadata 에 테이블 등록."""
    # In case this module is imported under a different app-dir (uvicorn reload),
    # ensure apps dir is present.
    if _APPS_DIR.exists() and str(_APPS_DIR) not in sys.path:
        sys.path.insert(0, str(_APPS_DIR))
    import users.app.dtos.schedule_access_grant_dto  # noqa: F401
    import users.app.dtos.schedule_access_dto  # noqa: F401
    import users.app.dtos.schedule_invite_code_dto  # noqa: F401
    import users.app.dtos.user_information_dto  # noqa: F401
    import users.app.dtos.user_dto  # noqa: F401
    import inbody.adapter.outbound.orm.community_orm  # noqa: F401
    import inbody.adapter.outbound.orm.notice_orm  # noqa: F401
    import inbody.adapter.outbound.orm.schedule_orm  # noqa: F401
    import inbody.adapter.outbound.orm.today_story_orm  # noqa: F401
    import inbody.adapter.outbound.orm.train_log_orm  # noqa: F401
    import inbody.adapter.outbound.orm.food_orm  # noqa: F401
    import titanic.adapter.outbound.orm.passenger_jack_trainer_orm  # noqa: F401
    import titanic.adapter.outbound.orm.passenger_rose_model_orm  # noqa: F401
    import comm_agent.adapter.outbound.orm.contact_orm  # noqa: F401
    import comm_agent.adapter.outbound.orm.received_mail_orm  # noqa: F401
    import comm_agent.adapter.outbound.orm.push_subscription_orm  # noqa: F401


async def create_database_tables() -> None:
    factory = get_async_session_factory()
    if factory is None or engine is None:
        return
    _import_orm_models()
    from sqlalchemy import text

    from core.matrix.theone_base import Base as TheoneBase
    async with engine.begin() as conn:
        # pgvector: Vector 컬럼을 쓰는 테이블 생성 전에 확장이 있어야 한다.
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(TheoneBase.metadata.create_all)


def create_database_tables_windows_threadsafe() -> None:
    """
    Windows + psycopg(async) 조합에서 uvicorn(ProactorEventLoop)로 실행될 때를 위해,
    SelectorEventLoop로 별도 실행합니다. (thread target으로 사용)
    """
    if sys.platform != "win32":
        raise RuntimeError("create_database_tables_windows_threadsafe is Windows-only")
    asyncio.run(
        create_database_tables(),
        loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()),
    )


__all__ = [
    "Base",
    "create_database_tables",
    "create_database_tables_windows_threadsafe",
    "get_async_session_factory",
    "get_db",
]

