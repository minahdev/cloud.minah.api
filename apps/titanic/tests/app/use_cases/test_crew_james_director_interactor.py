import pytest
from unittest.mock import AsyncMock, MagicMock

from titanic.app.use_cases.crew_james_director_interactor import JamesDirectorInteractor
from titanic.app.dtos.crew_james_director_dto import JamesDirectorQuery, JamesIntroduceResponse
from titanic.adapter.inbound.api.schemas.crew_james_director_schema import (
    FileUploadSchema,
    JamesDirectorSchema,
)


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.introduce_myself = AsyncMock(
        return_value=JamesIntroduceResponse(id=0, name="", answer="안녕하세요, 제임스입니다.")
    )
    repo.receive_uploaded_records = AsyncMock(return_value=3)
    return repo


@pytest.fixture
def interactor(mock_repository):
    return JamesDirectorInteractor(repository=mock_repository)


def _schema(**overrides) -> FileUploadSchema:
    defaults = dict(
        passenger_id="1",
        survived="0",
        pclass="3",
        name="Braund, Mr. Owen",
        gender="male",
        age="22",
        sib_sp="1",
        parch="0",
        ticket="A/5 21171",
        fare="7.25",
        cabin=None,
        embarked="S",
    )
    defaults.update(overrides)
    return FileUploadSchema(**defaults)


class TestIntroduceMyself:
    async def test_calls_repository_with_correct_query(self, interactor, mock_repository):
        schema = JamesDirectorSchema(id=4, name="James Cameron")

        await interactor.introduce_myself(schema)

        mock_repository.introduce_myself.assert_called_once_with(
            JamesDirectorQuery(id=4, name="James Cameron")
        )

    async def test_returns_repository_response(self, interactor):
        response = await interactor.introduce_myself(JamesDirectorSchema(id=4, name="James Cameron"))

        assert response.answer == "안녕하세요, 제임스입니다."


class TestUploadTitanicFile:
    async def test_creates_one_passenger_command_per_record(self, interactor, mock_repository):
        await interactor.upload_titanic_file([_schema(passenger_id="1"), _schema(passenger_id="2")])

        person_commands, _ = mock_repository.receive_uploaded_records.call_args.args
        assert len(person_commands) == 2

    async def test_passenger_command_contains_correct_fields(self, interactor, mock_repository):
        await interactor.upload_titanic_file([_schema(passenger_id="7", gender="female", age="28")])

        person_commands, _ = mock_repository.receive_uploaded_records.call_args.args
        cmd = person_commands[0]
        assert cmd.passenger_id == "7"
        assert cmd.gender == "female"
        assert cmd.age == "28"

    async def test_booking_command_contains_correct_fields(self, interactor, mock_repository):
        await interactor.upload_titanic_file([_schema(pclass="1", fare="100.0", embarked="C")])

        _, booking_commands = mock_repository.receive_uploaded_records.call_args.args
        cmd = booking_commands[0]
        assert cmd.pclass == "1"
        assert cmd.fare == "100.0"
        assert cmd.embarked == "C"

    async def test_none_fields_become_empty_string(self, interactor, mock_repository):
        # None 값은 빈 문자열로 변환돼야 DB 커맨드가 일관성 유지
        await interactor.upload_titanic_file([_schema(survived=None, cabin=None)])

        person_commands, booking_commands = mock_repository.receive_uploaded_records.call_args.args
        assert person_commands[0].survived == ""
        assert booking_commands[0].cabin == ""

    async def test_returns_saved_count_from_repository(self, interactor):
        result = await interactor.upload_titanic_file([_schema()])

        assert result == {"saved": 3}