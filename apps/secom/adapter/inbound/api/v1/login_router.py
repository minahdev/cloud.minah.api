from secom.adapter.input.login_use_case import LoginUseCase
from fastapi import APIRouter

login_router = APIRouter(prefix="/login", tags=["login"])

@signup_router.post("/login")
async def login(request: LoginRequest):
    pass