from dataclasses import dataclass


@dataclass(frozen=True)
class LoginQuery:
    user_id: str


@dataclass(frozen=True)
class LoginResult:
    user_id: str
    role: str
