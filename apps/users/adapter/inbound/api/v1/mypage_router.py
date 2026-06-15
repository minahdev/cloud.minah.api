from fastapi import APIRouter, Depends

from users.adapter.inbound.api.schemas.mypage_schema import MyPageProfileResponse, MyPageProfileSchema
from users.app.ports.input.mypage_use_case import MyPageUseCase
from users.dependencies.mypage_provider import get_mypage_use_case

mypage_router = APIRouter(prefix="/mypage", tags=["mypage"])


@mypage_router.get("/profile/{user_id}", response_model=MyPageProfileResponse)
async def get_profile(
    user_id: str,
    use_case: MyPageUseCase = Depends(get_mypage_use_case),
) -> MyPageProfileResponse:
    profile = await use_case.get_profile(user_id)
    return profile or MyPageProfileResponse(userId=user_id)


@mypage_router.put("/profile")
async def save_profile(
    schema: MyPageProfileSchema,
    use_case: MyPageUseCase = Depends(get_mypage_use_case),
) -> dict:
    await use_case.save_profile(schema)
    return {"message": "ok"}
