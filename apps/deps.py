from core.matrix.oracle_database import get_db
from core.matrix.keymaker_api import Keymaker, get_keymaker


def inject_keymaker() -> Keymaker:
    """FastAPI DI: 앱 전역 싱글톤 Keymaker."""
    return get_keymaker()
