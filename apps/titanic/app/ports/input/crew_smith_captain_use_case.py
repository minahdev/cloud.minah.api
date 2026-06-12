from abc import ABC, abstractmethod
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema, ChatSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse

class SmithCaptainUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: SmithCaptainSchema)-> SmithCaptainResponse:
        pass

    @abstractmethod
    async def chat(self, schema: ChatSchema,
                   rose: RoseModelUseCase,
                   jack: JackTrainerUseCase
                     
            ) -> SmithCaptainResponse:
        pass