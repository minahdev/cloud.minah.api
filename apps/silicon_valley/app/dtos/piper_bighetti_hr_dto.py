from dataclasses import dataclass

@dataclass(frozen=True)
class BighettiHrQuery:

    id: int
    name: str


@dataclass(frozen=True)
class BighettiHrResponse:

    id: int
    name: str
