from matrix.app.keymaker import get_keymaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

_engine = None
_session_factory = None

Base = declarative_base()


def _normalize_database_url(url: str) -> str:
    if "+psycopg" not in url:
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url


def get_async_session_factory():
    """Lazy init. Returns None if DATABASE_URL is missing (app can still start)."""
    global _engine, _session_factory
    if _session_factory is not None:
        return _session_factory
    raw = get_keymaker().database_url
    if not raw:
        return None
    url = _normalize_database_url(raw)
    _engine = create_async_engine(url, echo=True)
    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return _session_factory


def get_engine():
    get_async_session_factory()
    return _engine


async def create_database_tables() -> bool:
    """Base에 등록된 모든 테이블 생성."""
    engine = get_engine()
    if engine is None:
        return False
    import secom.app.models.user_model  # noqa: F401 — metadata 등록

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return True
