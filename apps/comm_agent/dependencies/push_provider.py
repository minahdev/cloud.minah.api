"""웹 푸시 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(PushSubscriptionRepository, WebPushSender)를 직접 알지 못한다.
- 세션은 core 의 get_db 에서 주입받는다.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from comm_agent.adapter.outbound.push.webpush_sender import WebPushSender
from comm_agent.adapter.outbound.repositories.push_subscription_repository import (
    PushSubscriptionRepository,
)
from comm_agent.app.ports.input.push_use_case import PushUseCase
from comm_agent.app.use_cases.push_interactor import PushInteractor


def get_push_use_case(db: AsyncSession = Depends(get_db)) -> PushUseCase:
    return PushInteractor(
        repository=PushSubscriptionRepository(session=db),
        sender=WebPushSender(),
    )
