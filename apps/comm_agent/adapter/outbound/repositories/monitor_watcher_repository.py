from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from comm_agent.app.dtos.monitor_watcher_dto import MonitorWatcherQuery, MonitorWatcherResponse
from comm_agent.app.ports.output.monitor_watcher_port import MonitorWatcherPort

import logging

logger = logging.getLogger(__name__)

class MonitorWatcherRepository(MonitorWatcherPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: MonitorWatcherQuery) -> MonitorWatcherResponse:
        
        '''모니터 왓쳐 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[MonitorWatcherRepository] 🍿introduce_myself 진입 | request_data={query}")
        
        response: MonitorWatcherResponse = MonitorWatcherResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response