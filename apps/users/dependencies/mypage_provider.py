"""
MyPage 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(UserInformationRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(MyPageUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db
from users.adapter.outbound.pg.user_pg_information_repository import UserInformationRepository
from users.app.ports.input.mypage_use_case import MyPageUseCase
from users.app.ports.output.mypage_repository import MyPageRepository
from users.app.use_cases.mypage_interactor import MyPageInteractor


def get_mypage_repository(
    db: AsyncSession = Depends(get_db),
) -> MyPageRepository:
    return UserInformationRepository(session=db)


def get_mypage_use_case(
    repository: MyPageRepository = Depends(get_mypage_repository),
) -> MyPageUseCase:
    return MyPageInteractor(repository=repository)
