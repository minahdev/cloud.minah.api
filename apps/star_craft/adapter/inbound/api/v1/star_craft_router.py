from __future__ import annotations

import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException

from comm_agent.app.dtos.email_send_dto import SendEmailResponse

from star_craft.adapter.inbound.api.schemas.compose_email_schema import ComposeEmailSchema
from star_craft.app.use_cases.compose_email_orchestrator import ComposeEmailOrchestrator
from star_craft.app.use_cases.sync_ontology_graph_interactor import SyncOntologyGraphInteractor
from star_craft.dependencies.compose_email_provider import get_compose_email_orchestrator
from star_craft.dependencies.ontology_graph_provider import get_sync_ontology_graph_use_case

logger = logging.getLogger(__name__)

star_craft_router = APIRouter(prefix="/star_craft", tags=["star_craft"])


@star_craft_router.post("/compose-email", response_model=SendEmailResponse)
async def compose_email(
    schema: ComposeEmailSchema,
    orchestrator: ComposeEmailOrchestrator = Depends(get_compose_email_orchestrator),
) -> SendEmailResponse:
    """주문을 받아 온톨로지 규격을 정하고 comm_agent에 작성·발송을 위임한다."""
    try:
        return await orchestrator.compose_and_send(
            to=schema.email,
            topic=schema.topic,
            email_type=schema.email_type,
            subject=schema.subject,
            sender_name=schema.sender_name,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"메일 발송(n8n) 오류: {e.response.status_code}",
        ) from e
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e).strip() or "메일 발송에 실패했습니다.",
        ) from e


@star_craft_router.post("/ontology/graph/sync")
async def sync_ontology_graph(
    use_case: SyncOntologyGraphInteractor = Depends(get_sync_ontology_graph_use_case),
) -> dict:
    """파이썬 온톨로지를 Neo4j 그래프로 적재한다. (이후 http://localhost:7474 에서 시각화)"""
    try:
        return await use_case.sync()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"Neo4j 적재 실패: {e}") from e
