"""
SQLAlchemy Base 클래스
루즈한 결합도로 설계 - 각 도메인이 독립적으로 사용 가능
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    모든 모델의 기본 클래스
    - 도메인 간 직접 의존 없음
    - 공통 기능은 믹스인으로 제공
    - 각 도메인은 독립적으로 진화 가능
    """
    pass