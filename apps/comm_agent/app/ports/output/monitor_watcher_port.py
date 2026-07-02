from abc import ABC, abstractmethod

from comm_agent.app.dtos.monitor_watcher_dto import MonitorWatcherQuery, MonitorWatcherResponse

class MonitorWatcherPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: MonitorWatcherQuery)-> MonitorWatcherResponse:
        pass