from pydantic import BaseModel


class SignupRequest(BaseModel):
    userId: str
    password: str
    nickname: str
    email: str
    role: str = "user"


class SignupResponse(BaseModel):
    message: str = "ok"
