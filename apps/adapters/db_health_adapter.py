from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseHealthAdapter:
    """Adapts SQLAlchemy async session to a simple health-check payload."""

    @staticmethod
    async def server_time_payload(db: AsyncSession) -> dict:
        try:
            result = await db.execute(text("SELECT NOW();"))
            now = result.scalar()
            return {"status": "success", "neon_time": now}
        except Exception as e:
            return {"status": "error", "message": str(e)}
