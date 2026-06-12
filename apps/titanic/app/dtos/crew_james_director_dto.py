from __future__ import annotations

from dataclasses import dataclass


@dataclass
class JamesDirectorQuery:
    id: str
    name: str


@dataclass
class PassengerCommand:
    """Person 테이블 — 3NF ERD 그대로 (타입은 str 통일)."""

    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass
class BookingCommand:
    """Booking + Port 역정규화 — `country` 제외 (타입은 str 통일)."""

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass
class JamesDirectorResponse:
    saved: int
    received: int
    message: str = "업로드가 완료되었습니다."


@dataclass
class JamesIntroduceResponse:
    id: int
    name: str
    answer: str = ""
