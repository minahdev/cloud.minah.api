from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.booking_orm import BookingModel
from titanic.adapter.outbound.orm.passenger_orm import PassengerModel
from titanic.app.dtos.crew_james_director_dto import BookingCommand, PassengerCommand
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository
from titanic.app.dtos.crew_james_director_dto import JamesDirectorResponse, JamesDirectorQuery, JamesIntroduceResponse

import logging

logger = logging.getLogger(__name__)


class JamesDirectorPgRepository(JamesDirectorRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    
    async def introduce_myself(self, query: JamesDirectorQuery) -> JamesIntroduceResponse:

        '''제임스 보트의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[JamesDirectorPgRepository] 🍗introduce_myself 진입 | request_data={query}")

        response = JamesIntroduceResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴"
        )

        return response






    async def upload_titanic_file(
        self,
        person_commands: list[PassengerCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        person_orms = [
            PassengerModel(
                passenger_id=cmd.passenger_id,
                name=cmd.name,
                gender=cmd.gender,
                age=cmd.age,
                sib_sp=cmd.sib_sp,
                parch=cmd.parch,
                survived=cmd.survived,
            )
            for cmd in person_commands
        ]
        self.session.add_all(person_orms)
        await self.session.flush()

        booking_orms = [
            BookingModel(
                passenger_id=person_orm.passenger_id,
                pclass=cmd.pclass,
                ticket=cmd.ticket,
                fare=cmd.fare,
                cabin=cmd.cabin,
                embarked=cmd.embarked,
            )
            for person_orm, cmd in zip(person_orms, booking_commands)
        ]
        self.session.add_all(booking_orms)
        await self.session.commit()

        return len(person_orms)