from dataclasses import dataclass

@dataclass(frozen=True)
class DineshDashQuery:

    id: int
    name: str


@dataclass(frozen=True)
class DineshDashResponse:

    id: int
    name: str
