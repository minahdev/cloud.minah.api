from pydantic import BaseModel


class PasswordVerifyRequest(BaseModel):
    userId: str
    password: str


class InviteCodeCreateRequest(BaseModel):
    coachUserId: str


class InviteCodeRedeemRequest(BaseModel):
    userId: str
    code: str


class SetPasswordRequest(BaseModel):
    coachUserId: str
    password: str


class InviteCodeResponse(BaseModel):
    code: str
    expiresAt: str


class AdmittedMemberItem(BaseModel):
    userId: str
    nickname: str


class AdmittedMembersResponse(BaseModel):
    members: list[AdmittedMemberItem]


class ScheduleAccessStatusResponse(BaseModel):
    isConfigured: bool
    message: str = "ok"
