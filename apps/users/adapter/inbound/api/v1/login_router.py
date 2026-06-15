from fastapi import APIRouter, Depends

from users.adapter.inbound.api.schemas.user_schema import LoginSchema
from users.app.dtos.login_dto import LoginResult
from users.app.ports.input.login_use_case import LoginUseCase
from users.dependencies.login_provider import get_login_use_case

login_router = APIRouter(prefix="/login", tags=["login"])


@login_router.post("", response_model=None)
async def login(
    schema: LoginSchema,
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> LoginResult:
    return await use_case.login_user(schema)
