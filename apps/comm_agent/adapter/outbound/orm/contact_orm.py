from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.theone_base import Base


class ContactOrm(Base):
    """주소록 1건 — Google 주소록 내보내기 CSV 컬럼 그대로 (titanic passengers 패턴).

    헤더 ↔ 컬럼 매핑:
      First Name→first_name … Nickname→nickname … E-mail 1 - Value→email …
    값은 titanic과 동일하게 문자열(String)로 통일한다.
    """

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 이름
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    name_prefix: Mapped[str | None] = mapped_column(String, nullable=True)
    name_suffix: Mapped[str | None] = mapped_column(String, nullable=True)
    nickname: Mapped[str | None] = mapped_column(String, nullable=True)
    file_as: Mapped[str | None] = mapped_column(String, nullable=True)

    # 조직
    organization_name: Mapped[str | None] = mapped_column(String, nullable=True)
    organization_title: Mapped[str | None] = mapped_column(String, nullable=True)
    organization_department: Mapped[str | None] = mapped_column(String, nullable=True)

    # 기타
    birthday: Mapped[str | None] = mapped_column(String, nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    photo: Mapped[str | None] = mapped_column(String, nullable=True)
    labels: Mapped[str | None] = mapped_column(String, nullable=True)

    # 이메일 (E-mail 1)
    email_1_label: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # E-mail 1 - Value

    # 전화 (Phone 1)
    phone_1_label: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_1_value: Mapped[str | None] = mapped_column(String, nullable=True)
