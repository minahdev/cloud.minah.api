"""`core.database` import 호환 — 실제 구현은 `core.matrix.database_manager`."""

from core.matrix.database_manager import (  # noqa: F401
    AsyncSessionLocal,
    Base,
    DATABASE_URL,
    create_database_tables,
    create_database_tables_windows_threadsafe,
    engine,
    get_async_session_factory,
    get_db,
)

__all__ = [
    "AsyncSessionLocal",
    "Base",
    "DATABASE_URL",
    "create_database_tables",
    "create_database_tables_windows_threadsafe",
    "engine",
    "get_async_session_factory",
    "get_db",
]
