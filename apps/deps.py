from core.matrix.secret_manager import Keymaker, get_keymaker


def inject_keymaker() -> Keymaker:
    """FastAPI DI: 앱 전역 싱글톤 Keymaker."""
    return get_keymaker()
