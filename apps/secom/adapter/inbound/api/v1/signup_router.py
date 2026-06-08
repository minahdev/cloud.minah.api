from secom.adapter.input.signup_use_case import SignupUseCase
from fastapi import APIRouter

signup_router = APIRouter(prefix="/signup", tags=["signup"])

@signup_router.post("/signup")
async def signup(request: SignupRequest):
    pass