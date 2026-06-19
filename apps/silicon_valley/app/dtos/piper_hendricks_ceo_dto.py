from dataclasses import dataclass

@dataclass(frozen=True)
class HendricksCeoQuery:

    id: int
    name: str


@dataclass(frozen=True)
class HendricksCeoResponse:

    id: int
    name: str
