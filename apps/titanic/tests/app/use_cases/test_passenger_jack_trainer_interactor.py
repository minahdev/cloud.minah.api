import pytest
from unittest.mock import AsyncMock, MagicMock

from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.introduce_myself = AsyncMock(
        return_value=JackTrainerResponse(id=9, name="Jack Dawson")
    )
    return repo


@pytest.fixture
def interactor(mock_repository):
    return JackTrainerInteractor(repository=mock_repository)


class TestIntroduceMyself:
    async def test_calls_repository_with_correct_query(self, interactor, mock_repository):
        schema = JackTrainerSchema(id=9, name="Jack Dawson")

        await interactor.introduce_myself(schema)

        mock_repository.introduce_myself.assert_called_once_with(
            JackTrainerQuery(id=9, name="Jack Dawson")
        )

    async def test_returns_repository_response(self, interactor):
        schema = JackTrainerSchema(id=9, name="Jack Dawson")

        response = await interactor.introduce_myself(schema)

        assert response == JackTrainerResponse(id=9, name="Jack Dawson")