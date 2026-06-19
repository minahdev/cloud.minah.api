from dataclasses import dataclass

@dataclass(frozen=True)
class GilfoyleSysQuery:

    id: int
    name: str


@dataclass(frozen=True)
class GilfoyleSysResponse:

    id: int
    name: str
