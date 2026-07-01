"""모니터(Monitor) 의존성 조립소 (DIP 팩토리).

- 라우터는 구현체(MonitorWatcherInteractor)를 직접 알지 못한다.
- 리턴 타입은 포트(MonitorWatcherUseCase)로 선언한다.
"""

from comm_agent.app.ports.input.monitor_watcher_use_case import MonitorWatcherUseCase
from comm_agent.app.use_cases.monitor_watcher_interactor import MonitorWatcherInteractor


def get_monitor_watcher_use_case() -> MonitorWatcherUseCase:
    return MonitorWatcherInteractor()
