from __future__ import annotations

import logging
import os

from neo4j import AsyncGraphDatabase

from star_craft.app.ports.output.ontology_graph_port import OntologyGraphPort

logger = logging.getLogger(__name__)


class Neo4jOntologyGraphAdapter(OntologyGraphPort):
    """온톨로지를 Neo4j 그래프로 적재한다.

    그래프 모델:
      (:Ontology)-[:HAS_CATEGORY]->(:SpamCategory)-[:HAS_KEYWORD]->(:Keyword)
      (:Ontology)-[:HAS_TYPE]->(:EmailType)-[:REQUIRES]->(:Element)
    접속값은 docker-compose의 neo4j 서비스 기본값을 사용한다.
    """

    def __init__(self) -> None:
        self._uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        self._user = os.getenv("NEO4J_USER", "neo4j")
        self._password = os.getenv("NEO4J_PASSWORD", "minah_password")

    async def sync_ontology(self, spam: list[dict], communication: list[dict]) -> dict:
        driver = AsyncGraphDatabase.driver(self._uri, auth=(self._user, self._password))
        try:
            async with driver.session() as session:
                # 기존 온톨로지 노드만 제거 (다른 데이터는 건드리지 않음)
                await session.run(
                    "MATCH (n) WHERE n:Ontology OR n:SpamCategory OR n:Keyword "
                    "OR n:EmailType OR n:Element DETACH DELETE n"
                )

                # 스팸 온톨로지
                await session.run("MERGE (:Ontology {name:'Spam'})")
                for c in spam:
                    await session.run(
                        "MATCH (o:Ontology {name:'Spam'}) "
                        "MERGE (cat:SpamCategory {name:$name}) "
                        "MERGE (o)-[:HAS_CATEGORY]->(cat) "
                        "WITH cat UNWIND $keywords AS kw "
                        "MERGE (k:Keyword {text:kw}) MERGE (cat)-[:HAS_KEYWORD]->(k)",
                        name=c["name"],
                        keywords=c["keywords"],
                    )

                # 커뮤니케이션 온톨로지
                await session.run("MERGE (:Ontology {name:'Communication'})")
                for t in communication:
                    await session.run(
                        "MATCH (o:Ontology {name:'Communication'}) "
                        "MERGE (et:EmailType {name:$name}) SET et.label=$label, et.tone=$tone "
                        "MERGE (o)-[:HAS_TYPE]->(et) "
                        "WITH et UNWIND $required AS el "
                        "MERGE (e:Element {text:el}) MERGE (et)-[:REQUIRES]->(e)",
                        name=t["name"],
                        label=t["label"],
                        tone=t["tone"],
                        required=t["required"],
                    )

                result = await session.run("MATCH (n) RETURN count(n) AS c")
                record = await result.single()
                nodes = record["c"] if record else 0
        finally:
            await driver.close()

        logger.info("[Neo4jOntologyGraph] 온톨로지 그래프 적재 완료 | nodes=%d", nodes)
        return {"nodes": nodes}
