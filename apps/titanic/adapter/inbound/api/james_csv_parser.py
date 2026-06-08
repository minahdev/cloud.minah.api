"""Titanic CSV 파싱 (무상태 inbound adapter)."""

from __future__ import annotations

import csv
from io import StringIO

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import TitanicRecordSchema

_ALLOWED_CONTENT_TYPES = frozenset(
    {"text/csv", "application/vnd.ms-excel", "text/plain", "application/csv"}
)


class JamesCsvParseError(ValueError):
    """CSV 검증·파싱 실패."""

    def __init__(self, message: str, *, line_no: int | None = None) -> None:
        self.line_no = line_no
        detail = f"CSV {line_no}행: {message}" if line_no is not None else message
        super().__init__(detail)


def assert_csv_upload(
    *,
    filename: str | None,
    content_type: str | None,
) -> None:
    """업로드 메타데이터만 검사 (I/O 없음)."""
    if filename and filename.lower().endswith(".csv"):
        return
    if content_type in _ALLOWED_CONTENT_TYPES:
        return
    raise JamesCsvParseError("CSV 파일을 업로드해주세요.")


def decode_csv_bytes(raw: bytes) -> str:
    """바이트 → UTF-8 텍스트 (BOM 허용)."""
    if not raw:
        raise JamesCsvParseError("빈 CSV 파일입니다.")
    text = raw.decode("utf-8-sig", errors="replace")
    if not text.strip():
        raise JamesCsvParseError("빈 CSV 파일입니다.")
    return text


def parse_titanic_csv_text(text: str) -> list[TitanicRecordSchema]:
    """CSV 텍스트 → 스키마 목록 (순수 함수, 요청 간 상태 없음)."""
    reader = csv.DictReader(StringIO(text))
    if not reader.fieldnames:
        raise JamesCsvParseError("CSV 헤더를 읽을 수 없습니다.")

    records: list[TitanicRecordSchema] = []
    for line_no, raw_row in enumerate(reader, start=2):
        if not any((value or "").strip() for value in raw_row.values()):
            continue
        try:
            records.append(TitanicRecordSchema.model_validate(raw_row))
        except Exception as exc:
            raise JamesCsvParseError(str(exc), line_no=line_no) from exc

    return records
