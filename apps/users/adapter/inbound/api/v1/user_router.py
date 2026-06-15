from fastapi import APIRouter, Depends

from users.app.ports.input.user_use_case import UserUseCase
from users.dependencies.user_provider import get_user_use_case

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/role/{user_id}")
async def get_user_role(
    user_id: str,
    use_case: UserUseCase = Depends(get_user_use_case),
) -> dict:
    role = await use_case.get_user_role(user_id)
    return {"userId": user_id, "role": role}
