"""온톨로지 그래프 적재 의존성 조립소 (Hub)."""

from fastapi import Depends

from star_craft.adapter.outbound.neo4j.ontology_graph_adapter import Neo4jOntologyGraphAdapter
from star_craft.app.ports.output.ontology_graph_port import OntologyGraphPort
from star_craft.app.use_cases.sync_ontology_graph_interactor import SyncOntologyGraphInteractor


def get_ontology_graph() -> OntologyGraphPort:
    return Neo4jOntologyGraphAdapter()


def get_sync_ontology_graph_use_case(
    graph: OntologyGraphPort = Depends(get_ontology_graph),
) -> SyncOntologyGraphInteractor:
    return SyncOntologyGraphInteractor(graph=graph)
