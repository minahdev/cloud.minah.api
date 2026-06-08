from __future__ import annotations

import logging

from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository
from titanic.adapter.inbound.api.schemas.crew_james_director_schema import TitanicRecordSchema
from titanic.app.dtos.crew_james_director_dto import (
    BookingCommand,
    JamesDirectorResponse,
    PersonCommand,
)

logger = logging.getLogger(__name__)


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesDirectorRepository) -> None:
        self._repository = repository

    async def upload_titanic_file(
        self, schema: list[TitanicRecordSchema]
    ) -> JamesDirectorResponse:
        print("[🤩제임스 유스케이스] : 업로드된 csv 파일에서 스키마로 옮겨진 상위 5개 레코드")
        for record in schema[:5]:
            print(record)

        person_commands: list[PersonCommand] = []
        booking_commands: list[BookingCommand] = []

        for record in schema:
            person_commands.append(
                PersonCommand(
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
        return JamesDirectorResponse(saved=saved, received=len(schema))
