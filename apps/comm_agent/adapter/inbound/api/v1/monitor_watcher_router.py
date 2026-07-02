from fastapi import APIRouter, Depends

from comm_agent.adapter.inbound.api.schemas.monitor_watcher_schema import MonitorWatcherSchema
from comm_agent.adapter.inbound.api.schemas.receive_mail_schema import ReceiveMailSchema
from comm_agent.app.dtos.monitor_watcher_dto import MonitorWatcherResponse
from comm_agent.app.dtos.received_mail_dto import ReceivedMailCommand
from comm_agent.app.ports.input.monitor_watcher_use_case import MonitorWatcherUseCase
from comm_agent.dependencies.monitor_watcher_provider import get_monitor_watcher_use_case

"""
모니터 (Monitor)
역할 (keyword): watcher (관찰/기록자)
시스템의 이벤트·로그·상태 변화를 관찰하고 기록하는 감시자.
"""

monitor_watcher_router = APIRouter(prefix="/comm_agent/monitor", tags=["comm_agent_monitor"])


@monitor_watcher_router.get("/myself", response_model=MonitorWatcherResponse)
async def introduce_myself(
    monitor: MonitorWatcherUseCase = Depends(get_monitor_watcher_use_case),
) -> MonitorWatcherResponse:
    return await monitor.introduce_myself(
        MonitorWatcherSchema(
            id=5,
            name="모니터 (Monitor)",
        )
    )


@monitor_watcher_router.post("/screen")
async def screen_mail(
    schema: ReceiveMailSchema,
    monitor: MonitorWatcherUseCase = Depends(get_monitor_watcher_use_case),
) -> dict:
    """인입 메일을 필터링해 정상건만 pgvector 파이프라인으로 전달한다."""
    return await monitor.screen_and_store(
        ReceivedMailCommand(
            sender=schema.from_,
            subject=schema.subject,
            body=schema.body,
        )
    )
