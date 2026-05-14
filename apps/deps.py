from fastapi import HTTPException

from database import get_async_session_factory


async def get_db():
    factory = get_async_session_factory()
    if factory is None:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL is not set or empty. Configure it to use the database.",
        )
    async with factory() as session:
        yield session
