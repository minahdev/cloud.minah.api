from __future__ import annotations

from pydantic import BaseModel, ConfigDict, model_validator


class ContactRecordSchema(BaseModel):
    """주소록 CSV 1행.

    지원 형식:
      - 단순: `닉네임,이메일` 또는 `nickname,email`
      - Google 주소록 내보내기: `First Name … Nickname … E-mail 1 - Value …`
    """

    model_config = ConfigDict(populate_by_name=True)

    nickname: str = ""
    email: str = ""

    @model_validator(mode="before")
    @classmethod
    def _normalize_row(cls, data):
        if not isinstance(data, dict):
            return data

        # 헤더 앞뒤 공백 제거 후 매핑
        row = {(k or "").strip(): (v or "").strip() for k, v in data.items()}

        def pick(*keys: str) -> str:
            for key in keys:
                if row.get(key):
                    return row[key]
            return ""

        email = pick("E-mail 1 - Value", "email", "이메일", "Email", "E-mail", "mail")

        nickname = pick("Nickname", "닉네임", "nickname", "File As", "이름", "name", "Name")
        if not nickname:
            # Google 내보내기: 이름 컬럼 조합
            parts = [row.get("First Name", ""), row.get("Middle Name", ""), row.get("Last Name", "")]
            nickname = " ".join(p for p in parts if p).strip()
        if not nickname:
            nickname = pick("Organization Name")

        return {"nickname": nickname, "email": email}


class UploadContactsResponseSchema(BaseModel):
    """POST /comm_agent/contacts/upload 응답."""

    saved: int
    message: str = "주소록 업로드가 완료되었습니다."


class ContactViewSchema(BaseModel):
    """GET /comm_agent/contacts 항목."""

    id: int
    nickname: str
    email: str


class ContactIntroduceSchema(BaseModel):
    """주소록(Address Book) 자기소개 입력."""

    id: int
    name: str
