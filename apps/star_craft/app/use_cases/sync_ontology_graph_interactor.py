from __future__ import annotations

import logging

from star_craft.app.ports.output.ontology_graph_port import OntologyGraphPort
from star_craft.domain.ontology.communication.email_template import COMMUNICATION_TAXONOMY
from star_craft.domain.ontology.spam.spam_taxonomy import SPAM_TAXONOMY

logger = logging.getLogger(__name__)


class SyncOntologyGraphInteractor:
    """파이썬 온톨로지(스팸·커뮤니케이션)를 읽어 그래프 저장소에 적재한다 (Hub 지식 인덱스)."""

    def __init__(self, graph: OntologyGraphPort) -> None:
        self._graph = graph

    async def sync(self) -> dict:
        spam = [
            {"name": concept.category.value, "keywords": list(concept.keywords)}
            for concept in SPAM_TAXONOMY
        ]
        communication = [
            {
                "name": email_type.value,
                "label": spec.type_label,
                "tone": spec.tone,
                "required": list(spec.required_elements),
            }
            for email_type, spec in COMMUNICATION_TAXONOMY.items()
        ]
        logger.info(
            "[SyncOntologyGraph] 적재 시작 | spam=%d개 category, communication=%d개 type",
            len(spam),
            len(communication),
        )
        return await self._graph.sync_ontology(spam, communication)
