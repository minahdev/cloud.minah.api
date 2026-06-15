from pydantic import BaseModel


class LoginRequest(BaseModel):
    userId: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
