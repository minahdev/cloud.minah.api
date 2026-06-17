"""Titanic ??PostgreSQL outbound adapters (`adapter/inbound/api/v1` ???."""

from titanic.adapter.outbound.repositories.crew_andrews_architect_repository import (
    AndrewsArchitectRepository,
)
from titanic.adapter.outbound.repositories.passenger_cal_tester_repository import CalTesterRepository
from titanic.adapter.outbound.repositories.crew_hartley_violin_repository import (
    HartleyViolinRepository,
)
from titanic.adapter.outbound.repositories.passenger_isidor_couple_repository import IsidorCoupleRepository
from titanic.adapter.outbound.repositories.passenger_jack_trainer_repository import JackTrainerRepository
from titanic.adapter.outbound.repositories.crew_james_director_repository import (
    JamesDirectorRepository,
)
from titanic.adapter.outbound.repositories.crew_lowe_boat_repository import LoweBoatRepository
from titanic.adapter.outbound.repositories.passenger_molly_scaler_repository import MollyScalerRepository
from titanic.adapter.outbound.repositories.passenger_rose_model_repository import RoseModelRepository
from titanic.adapter.outbound.repositories.passenger_ruth_validation_repository import RuthValidationRepository
from titanic.adapter.outbound.repositories.crew_smith_captain_repository import (
    SmithCaptainRepository,
)
from titanic.adapter.outbound.repositories.crew_walter_roaster_repository import (
    WalterRoasterRepository,
)

__all__ = [
    "AndrewsArchitectRepository",
    "CalTesterRepository",
    "HartleyViolinRepository",
    "IsidorCoupleRepository",
    "JackTrainerRepository",
    "JamesDirectorRepository",
    "LoweBoatRepository",
    "MollyScalerRepository",
    "RoseModelRepository",
    "RuthValidationRepository",
    "SmithCaptainRepository",
    "WalterRoasterRepository",
]
