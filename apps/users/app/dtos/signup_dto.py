from dataclasses import dataclass


@dataclass(frozen=True)
class SignupCommand:
    user_id: str
    password_hash: str
    email: str
    nickname: str
    role: str


@dataclass(frozen=True)
class SignupResult:
    user_id: str
    message: str = "회원가입이 완료되었습니다."
