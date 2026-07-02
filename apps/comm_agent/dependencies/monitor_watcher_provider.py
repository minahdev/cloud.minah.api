"""모니터(Monitor) 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(MonitorWatcherRepository·KorUnsmileSpamFilter)를 직접 알지 못한다.
- 리턴 타입은 포트(MonitorWatcherUseCase)로 선언한다.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.database_manager import get_db

from comm_agent.adapter.outbound.filter.kor_unsmile_filter import KorUnsmileSpamFilter
from comm_agent.adapter.outbound.repositories.monitor_watcher_repository import (
    MonitorWatcherRepository,
)
from comm_agent.app.ports.input.monitor_watcher_use_case import MonitorWatcherUseCase
from comm_agent.app.ports.input.received_mail_use_case import ReceiveMailUseCase
from comm_agent.app.ports.output.monitor_watcher_port import MonitorWatcherPort
from comm_agent.app.ports.output.spam_filter_port import SpamFilterPort
from comm_agent.app.use_cases.monitor_watcher_interactor import MonitorWatcherInteractor
from comm_agent.dependencies.received_mail_provider import get_receive_mail_use_case


def get_monitor_watcher_repository(db: AsyncSession = Depends(get_db)) -> MonitorWatcherPort:
    return MonitorWatcherRepository(session=db)


def get_spam_filter() -> SpamFilterPort:
    return KorUnsmileSpamFilter()


def get_monitor_watcher_use_case(
    repository: MonitorWatcherPort = Depends(get_monitor_watcher_repository),
    spam_filter: SpamFilterPort = Depends(get_spam_filter),
    receive_mail: ReceiveMailUseCase = Depends(get_receive_mail_use_case),
) -> MonitorWatcherUseCase:
    return MonitorWatcherInteractor(
        repository=repository,
        spam_filter=spam_filter,
        receive_mail=receive_mail,
    )
