from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import JamesDirectorSchema, TitanicRecordSchema
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.crew_james_director_port import JamesDirectorPort
from titanic.app.dtos.crew_james_director_dto import (
    BookingCommand,
    JamesDirectorQuery,
    JamesDirectorResponse,
    JamesIntroduceResponse,
    PassengerCommand,
)

logger = logging.getLogger(__name__)


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesDirectorPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: JamesDirectorSchema) -> JamesIntroduceResponse:

        return await self._repository.introduce_myself(JamesDirectorQuery(
            id= schema.id,
            name= schema.name
        ))

    async def upload_titanic_file(
        self, schema: list[TitanicRecordSchema]
    ) -> JamesDirectorResponse:
        print("[🤩제임스 유스케이스] : 업로드된 csv 파일에서 스키마로 옮겨진 상위 5개 레코드")
        for record in schema[:5]:
            print(record)

        person_commands: list[PassengerCommand] = []
        booking_commands: list[BookingCommand] = []

        for record in schema:
            person_commands.append(
                PassengerCommand(
                    passenger_id=record.passenger_id or "",
                    name=record.name or "",
                    gender=record.gender or "",
                    age=record.age or "",
                    sib_sp=record.sib_sp or "",
                    parch=record.parch or "",
                    survived=record.survived or "",
                )
            )
            booking_commands.append(
                BookingCommand(
                    pclass=record.pclass or "",
                    ticket=record.ticket or "",
                    fare=record.fare or "",
                    cabin=record.cabin or "",
                    embarked=record.embarked or "",
                )
            )

        saved = await self._repository.upload_titanic_file(
            person_commands, booking_commands
        )

        return {"saved": saved}