from fastapi import APIRouter, Depends

from users.adapter.inbound.api.schemas.schedule_access_schema import (
    AdmittedMembersResponse,
    AdmittedMemberItem,
    InviteCodeCreateRequest,
    InviteCodeRedeemRequest,
    InviteCodeResponse,
    PasswordVerifyRequest,
    ScheduleAccessStatusResponse,
    SetPasswordRequest,
)
from users.app.ports.input.schedule_access_use_case import ScheduleAccessUseCase
from users.dependencies.schedule_access_provider import get_schedule_access_use_case

schedule_access_router = APIRouter(prefix="/schedule-access", tags=["schedule-access"])


@schedule_access_router.get("/status")
async def get_status(
    use_case: ScheduleAccessUseCase = Depends(get_schedule_access_use_case),
) -> ScheduleAccessStatusResponse:
    is_configured = await use_case.is_configured()
    return ScheduleAccessStatusResponse(isConfigured=is_configured)


@schedule_access_router.post("/verify-password")
async def verify_and_grant(
    schema: PasswordVerifyRequest,
    use_case: ScheduleAccessUseCase = Depends(get_schedule_access_use_case),
) -> dict:
    await use_case.verify_and_grant(schema.userId, schema.password)
    return {"message": "ok"}


@schedule_access_router.post("/invite-code")
async def create_invite_code(
    schema: InviteCodeCreateRequest,
    use_case: ScheduleAccessUseCase = Depends(get_schedule_access_use_case),
) -> InviteCodeResponse:
    result = await use_case.create_invite_code(schema.coachUserId)
    return InviteCodeResponse(code=result["code"], expiresAt=result["expiresAt"])


@schedule_access_router.post("/redeem")
async def redeem_invite_code(
    schema: InviteCodeRedeemRequest,
    use_case: ScheduleAccessUseCase = Depends(get_schedule_access_use_case),
) -> dict:
    await use_case.redeem_invite_code(schema.userId, schema.code)
    return {"message": "ok"}


@schedule_access_router.put("/password")
async def set_password(
    schema: SetPasswordRequest,
    use_case: ScheduleAccessUseCase = Depends(get_schedule_access_use_case),
) -> dict:
    await use_case.set_password(schema.coachUserId, schema.password)
    return {"message": "ok"}


@schedule_access_router.get("/members")
async def list_admitted_members(
    requesterUserId: str,
    use_case: ScheduleAccessUseCase = Depends(get_schedule_access_use_case),
) -> AdmittedMembersResponse:
    rows = await use_case.list_admitted_members_for_coach(requesterUserId)
    return AdmittedMembersResponse(members=[AdmittedMemberItem(**r) for r in rows])
