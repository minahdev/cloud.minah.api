"""주소록 CSV 파싱 (무상태 inbound adapter) — titanic james_csv_parser 패턴."""

from __future__ import annotations

import csv
from io import StringIO

from comm_agent.adapter.inbound.api.schemas.contact_schema import ContactRecordSchema


class ContactCsvParseError(ValueError):
    """CSV 검증·파싱 실패."""

    def __init__(self, message: str, *, line_no: int | None = None) -> None:
        self.line_no = line_no
        detail = f"CSV {line_no}행: {message}" if line_no is not None else message
        super().__init__(detail)


def parse_contacts_csv_text(text: str) -> list[ContactRecordSchema]:
    """CSV 텍스트 → 스키마 목록 (순수 함수)."""
    if not text.strip():
        raise ContactCsvParseError("빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if not reader.fieldnames:
        raise ContactCsvParseError("CSV 헤더를 읽을 수 없습니다.")

    records: list[ContactRecordSchema] = []
    for line_no, raw_row in enumerate(reader, start=2):
        if not any((value or "").strip() for value in raw_row.values()):
            continue
        try:
            record = ContactRecordSchema.model_validate(raw_row)
        except Exception as exc:
            raise ContactCsvParseError(str(exc), line_no=line_no) from exc
        # 이메일 없는 연락처(구글 내보내기에 흔함)는 건너뛴다.
        if not record.email.strip():
            continue
        records.append(record)

    if not records:
        raise ContactCsvParseError("이메일이 있는 주소록 데이터가 없습니다.")
    return records
