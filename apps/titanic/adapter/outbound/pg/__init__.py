"""Titanic — PostgreSQL outbound adapters (`adapter/inbound/api/v1` 대응)."""

from titanic.adapter.outbound.pg.crew_andrews_architect_pg_repository import (
    AndrewsArchitectPgRepository,
)
from titanic.adapter.outbound.pg.passenger_cal_tester_pg_repository import CalTesterPgRepository
from titanic.adapter.outbound.pg.crew_hartley_violin_pg_repository import (
    HartleyViolinPgRepository,
)
from titanic.adapter.outbound.pg.passenger_isidor_couple_pg_repository import IsidorCouplePgRepository
from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackTrainerPgRepository
from titanic.adapter.outbound.pg.crew_james_director_pg_repository import (
    JamesDirectorPgRepository,
)
from titanic.adapter.outbound.pg.crew_lowe_boat_pg_repository import LoweBoatPgRepository
from titanic.adapter.outbound.pg.passenger_molly_scaler_pg_repository import MollyScalerPgRepository
from titanic.adapter.outbound.pg.passenger_rose_model_pg_repository import RoseModelPgRepository
from titanic.adapter.outbound.pg.passenger_ruth_validation_pg_repository import RuthValidationPgRepository
from titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import (
    SmithCaptainPgRepository,
)
from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import (
    WalterRoasterPgRepository,
)

__all__ = [
    "AndrewsArchitectPgRepository",
    "CalTesterPgRepository",
    "HartleyViolinPgRepository",
    "IsidorCouplePgRepository",
    "JackTrainerPgRepository",
    "JamesDirectorPgRepository",
    "LoweBoatPgRepository",
    "MollyScalerPgRepository",
    "RoseModelPgRepository",
    "RuthValidationPgRepository",
    "SmithCaptainPgRepository",
    "WalterRoasterPgRepository",
]
