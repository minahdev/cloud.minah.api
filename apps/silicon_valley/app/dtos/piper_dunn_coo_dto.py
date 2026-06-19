from dataclasses import dataclass

@dataclass(frozen=True)
class DunnCooQuery:

    id: int
    name: str


@dataclass(frozen=True)
class DunnCooResponse:

    id: int
    name: str
