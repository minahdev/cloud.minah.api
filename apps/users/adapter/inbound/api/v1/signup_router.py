from fastapi import APIRouter, Depends

from users.adapter.inbound.api.schemas.user_schema import UserSchema
from users.app.dtos.signup_dto import SignupResult
from users.app.ports.input.signup_use_case import SignupUseCase
from users.dependencies.signup_provider import get_signup_use_case

signup_router = APIRouter(prefix="/signup", tags=["signup"])


@signup_router.post("", response_model=None)
async def signup(
    schema: UserSchema,
    use_case: SignupUseCase = Depends(get_signup_use_case),
) -> SignupResult:
    return await use_case.save_user(schema)


@signup_router.get("/check-id")
async def check_user_id(
    userId: str,
    use_case: SignupUseCase = Depends(get_signup_use_case),
) -> dict:
    available = await use_case.is_user_id_available(userId)
    return {"available": available}
