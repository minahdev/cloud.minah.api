"""Neon PostgreSQL async engine, session, and SQLAlchemy 2.0 DeclarativeBase."""

import asyncio
import os
from collections.abc import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from matrix.app.keymaker import get_keymaker

_engine = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 declarative base — ORM models must inherit this."""


def _normalize_database_url(url: str) -> str:
    """Neon URL → async driver (postgresql+psycopg)."""
    if "+psycopg" not in url:
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url


def get_database_url() -> str | None:
    raw = get_keymaker().database_url
    if not raw or not str(raw).strip():
        return None
    return _normalize_database_url(str(raw).strip())


def _sqlalchemy_echo() -> bool:
    """Set DATABASE_ECHO=true in backend/.env to log every SQL statement."""
    return os.getenv("DATABASE_ECHO", "").strip().lower() in ("1", "true", "yes")


def get_async_session_factory() -> async_sessionmaker[AsyncSession] | None:
    """Lazy init from backend/.env DATABASE_URL. None if unset."""
    global _engine, _session_factory
    if _session_factory is not None:
        return _session_factory
    url = get_database_url()
    if not url:
        return None
    _engine = create_async_engine(url, echo=_sqlalchemy_echo())
    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return _session_factory


def get_engine():
    get_async_session_factory()
    return _engine


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    factory = get_async_session_factory()
    if factory is None:
        raise RuntimeError("DATABASE_URL is not set in backend/.env")
    async with factory() as session:
        yield session


async def create_database_tables() -> bool:
    """Create all tables registered on Base.metadata."""
    engine = get_engine()
    if engine is None:
        return False
    import secom.app.models.user_information_model  # noqa: F401
    import secom.app.models.user_model  # noqa: F401 — register ORM models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return True


async def main() -> None:
    """
    Neon 연결 확인용 샘플 (apps 디렉터리에서):
      python database.py
    """
    import secom.app.models.user_model as user_model  # noqa: F401

    url = get_database_url()
    if not url:
        raise RuntimeError("DATABASE_URL is not set in backend/.env")

    engine = create_async_engine(url, echo=_sqlalchemy_echo())

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        demo = user_model.User(
            user_id="demo_user",
            password_hash="hashed_placeholder",
            email="demo@pace.dev",
            nickname="데모",
            role="user",
        )
        session.add(demo)
        await session.commit()

        stmt = select(user_model.User).where(user_model.User.role == "user")
        result = await session.execute(stmt)
        users = result.scalars().all()
        for u in users:
            print(f"조회된 유저: {u.user_id} | {u.nickname} | {u.email}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
