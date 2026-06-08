"""Titanic — PostgreSQL outbound adapters (`adapter/inbound/api/v1` 대응)."""

from titanic.adapter.outbound.pg.crew_andrews_architect_pg_repository import (
    AndrewsBlueprintPgRepository,
)
from titanic.adapter.outbound.pg.passenger_cal_tester_pg_repository import CalPistolPgRepository
from titanic.adapter.outbound.pg.crew_hartley_violin_pg_repository import (
    HartleyViolinPgRepository,
)
from titanic.adapter.outbound.pg.passenger_isidor_couple_pg_repository import IsidorBedPgRepository
from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackSketchPgRepository
from titanic.adapter.outbound.pg.crew_james_director_pg_repository import (
    JamesDirectorPgRepository,
)
from titanic.adapter.outbound.pg.passenger_rose_model_pg_repository import RoseDiamondPgRepository
from minahai.apps.titanic.adapter.outbound.pg.passenger_ruth_validation_pg_repository import RuthCorsetPgRepository
from titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import (
    SmithCaptainPgRepository,
)
from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import (
    WalterRoasterPgRepository,
)

__all__ = [
    "AndrewsBlueprintPgRepository",
    "CalPistolPgRepository",
    "HartleyViolinPgRepository",
    "IsidorBedPgRepository",
    "JackSketchPgRepository",
    "JamesDirectorPgRepository",
    "RoseDiamondPgRepository",
    "RuthCorsetPgRepository",
    "SmithCaptainPgRepository",
    "WalterRoasterPgRepository",
]
