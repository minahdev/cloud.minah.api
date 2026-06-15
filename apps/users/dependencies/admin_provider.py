"""
Admin 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(AdminService)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(AdminUseCase)로 선언한다.
"""

from users.app.ports.input.admin_use_case import AdminUseCase
from users.app.use_cases.admin_interactor import AdminService


def get_admin_use_case() -> AdminUseCase:
    return AdminService()
