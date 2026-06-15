from users.adapter.inbound.api.schemas.mypage_schema import MyPageProfileResponse, MyPageProfileSchema
from users.app.ports.input.mypage_use_case import MyPageUseCase
from users.app.ports.output.mypage_repository import MyPageRepository


class MyPageInteractor(MyPageUseCase):

    def __init__(self, repository: MyPageRepository) -> None:
        self._repository = repository

    async def get_profile(self, user_id: str) -> MyPageProfileResponse | None:
        return await self._repository.get_profile(user_id)

    async def save_profile(self, profile: MyPageProfileSchema) -> None:
        await self._repository.save_profile(profile)
