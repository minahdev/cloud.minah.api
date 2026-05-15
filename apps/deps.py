from fastapi import HTTPException

from database import get_async_session_factory
from matrix.app.keymaker import Keymaker, get_keymaker


def inject_keymaker() -> Keymaker:
    """FastAPI DI: 앱 전역 싱글톤 Keymaker."""
    return get_keymaker()


async def get_db():
    factory = get_async_session_factory()
    if factory is None:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL is not set or empty. Configure it to use the database.",
        )
    async with factory() as session:
        yield session
