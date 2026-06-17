from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm as BookingModel
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PassengerModel
from titanic.app.dtos.crew_james_director_dto import BookingCommand, PassengerCommand
from titanic.app.ports.output.crew_james_director_port import JamesDirectorPort
from titanic.app.dtos.crew_james_director_dto import JamesDirectorResponse, JamesDirectorQuery, JamesIntroduceResponse

import logging

logger = logging.getLogger(__name__)


class JamesDirectorRepository(JamesDirectorPort):
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
        person_values = [
            {
                "passenger_id": cmd.passenger_id,
                "name": cmd.name,
                "gender": cmd.gender,
                "age": cmd.age,
                "sib_sp": cmd.sib_sp,
                "parch": cmd.parch,
                "survived": cmd.survived,
            }
            for cmd in person_commands
        ]
        await self.session.execute(
            insert(PassengerModel).values(person_values).on_conflict_do_nothing(index_elements=["passenger_id"])
        )
        await self.session.flush()

        booking_values = [
            {
                "passenger_id": cmd_p.passenger_id,
                "pclass": cmd_b.pclass or "",
                "ticket": cmd_b.ticket or "",
                "fare": cmd_b.fare or "",
                "cabin": cmd_b.cabin or "",
                "embarked": cmd_b.embarked or "",
            }
            for cmd_p, cmd_b in zip(person_commands, booking_commands)
        ]
        await self.session.execute(
            insert(BookingModel).values(booking_values)
        )
        await self.session.commit()

        return len(person_values)