import asyncio
import sys
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

# Ensure `backend/` and `backend/apps/` are importable regardless of uvicorn app-dir.
_BACKEND_DIR = Path(__file__).resolve().parent
_APPS_DIR = _BACKEND_DIR / "apps"
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))
if _APPS_DIR.exists() and str(_APPS_DIR) not in sys.path:
    sys.path.insert(0, str(_APPS_DIR))

if sys.platform == "win32":
    # psycopg async requires SelectorEventLoop on Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.db_health_adapter import DatabaseHealthAdapter
from deps import inject_keymaker
from core.matrix.keymaker_api import Keymaker, is_gemini_quota_error
from doro.app.doro_diretor import Diretor
from chat_mirror import get_last_chat, record_chat
from weather.app.weather_controller import WeatherController
from core.database import (
    create_database_tables,
    create_database_tables_windows_threadsafe,
    get_db,
)
from secom.adapter.inbound.api.schemas.mypage_schema import (
    MyPageProfileResponse,
    MyPageProfileSchema,
)
from secom.adapter.inbound.api.schemas.user_schema import LoginSchema, UserSchema
from secom.app.use_cases.schedule_access_interactor import ScheduleAccessService
from secom.app.use_cases.user_interactor import UserService
from inbody.community_media import get_community_media_storage
from inbody.router import router as inbody_router
from titanic.adapter.inbound.api import titanic_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
    force=True,
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_community_media_storage().ensure_dir()
    if sys.platform == "win32":
        await asyncio.to_thread(create_database_tables_windows_threadsafe)
    else:
        await create_database_tables()
    yield


app = FastAPI(title="Minahdev Cloud Main Page", lifespan=lifespan)
app.include_router(inbody_router)
app.include_router(titanic_router)

_UPLOADS_ROOT = Path(__file__).resolve().parent / "uploads"
_UPLOADS_ROOT.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_UPLOADS_ROOT)), name="uploads")


class ChatMessage(BaseModel):
    role: Literal["user", "model"]
    text: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1)


class ChatResponse(BaseModel):
    text: str


class LastChatResponse(BaseModel):
    """프론트 POST /chat 이후 저장된 최근 질문·답변."""

    user_text: str | None = None
    model_text: str | None = None
    model_name: str | None = None
    updated_at: str | None = None


class SignupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    userId: str = Field(..., min_length=1, max_length=64, alias="userId")
    password: str = Field(..., min_length=1, max_length=128)
    email: str = Field(..., min_length=3, max_length=254, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    nickname: str = Field(..., min_length=1, max_length=64)
    role: Literal["user", "admin", "coach"] = "user"


class SignupResponse(BaseModel):
    message: str
    userId: str
    email: str
    nickname: str
    role: str = "user"


class UserIdCheckResponse(BaseModel):
    userId: str
    available: bool
    message: str

class LoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    userId: str = Field(..., min_length=1, max_length=64, alias="userId")
    password: str = Field(..., min_length=1, max_length=128)


class LoginResponse(BaseModel):
    message: str
    userId: str
    role: str = "user"


class WeatherResponse(BaseModel):
    city: str
    temp_c: float | None = None
    feels_like_c: float | None = None
    humidity: int | None = None
    description: str = ""
    icon: str | None = None
    lat: float | None = None
    lon: float | None = None


# 메인 페이지(CurrentWeather)에서 마지막으로 조회한 날씨
_main_page_weather: dict | None = None


@app.get("/weather", response_model=WeatherResponse)
def get_weather(
    lat: float | None = None,
    lon: float | None = None,
    city: str | None = None,
    km: Keymaker = Depends(inject_keymaker),
) -> WeatherResponse:
    """현재 위치(lat/lon) 또는 도시명으로 날씨 조회 (OpenWeatherMap)."""
    global _main_page_weather

    if lat is None and lon is None and not (city and city.strip()):
        if _main_page_weather is not None:
            return WeatherResponse(**_main_page_weather)
        raise HTTPException(
            status_code=404,
            detail="메인 페이지에서 날씨가 로드된 뒤 다시 접속하세요.",
        )

    if not km.has_weather_api_key:
        raise HTTPException(
            status_code=503,
            detail="'.env'에 WEATHER_API_KEY를 설정하세요.",
        )

    controller = WeatherController(km)
    try:
        if lat is not None and lon is not None:
            payload = controller.get_by_coordinates(lat, lon)
        elif city and city.strip():
            payload = controller.get_by_city(city.strip())
        else:
            raise HTTPException(status_code=400, detail="lat·lon 또는 city가 필요합니다.")
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"날씨 API 오류: {e.response.status_code}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=str(e).strip() or "날씨 조회에 실패했습니다.",
        ) from e

    _main_page_weather = payload
    return WeatherResponse(**payload)


@app.get("/chat", response_model=LastChatResponse)
def get_chat() -> LastChatResponse:
    """프론트 Gemini 채팅과 동기화된 최근 질문·답변 (JSON)."""
    snap = get_last_chat()
    if snap is None:
        return LastChatResponse()
    return LastChatResponse(**snap.to_dict())


@app.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    km: Keymaker = Depends(inject_keymaker),
) -> ChatResponse:
    if km.gemini_model is None:
        raise HTTPException(
            status_code=503,
            detail="'.env'에 GEMINI_API_KEY를 설정하세요.",
        )

    msgs = req.messages
    last = msgs[-1]
    if last.role != "user":
        raise HTTPException(status_code=400, detail="마지막 메시지는 role이 'user'여야 합니다.")

    history: list[dict] = []
    for m in msgs[:-1]:
        role = "user" if m.role == "user" else "model"
        history.append({"role": role, "parts": m.text})

    try:
        text, _model_used = km.send_chat(history=history, user_text=last.text)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=429, detail=str(e)) from e
    except Exception as e:
        msg = str(e).strip() or "Gemini 요청에 실패했습니다."
        if is_gemini_quota_error(e):
            raise HTTPException(status_code=429, detail=msg) from e
        raise HTTPException(status_code=502, detail=msg) from e

    if not text:
        raise HTTPException(status_code=502, detail="Gemini 응답이 비어 있습니다.")

    record_chat(user_text=last.text, model_text=text, model_name=_model_used)
    return ChatResponse(text=text)

@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}

@app.get("/doro/data")
def read_doro_data():
    diretor = Diretor()
    try:
        df = diretor.get_data_doro()
        return df.to_dict(orient="records")
    except RuntimeError as e:
        raise HTTPException(status_code=501, detail=str(e)) from e


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DatabaseHealthAdapter.server_time_payload(db)



@app.get("/signup/check-userid", response_model=UserIdCheckResponse)
async def check_signup_user_id(userId: str, db: AsyncSession = Depends(get_db)) -> UserIdCheckResponse:
    """회원가입 전 아이디 중복 확인."""
    user_id = userId.strip()
    if not user_id:
        raise HTTPException(status_code=400, detail="userId가 필요합니다.")

    user_controller = UserService(db)
    available = await user_controller.is_user_id_available(user_id)
    return UserIdCheckResponse(
        userId=user_id,
        available=available,
        message="사용 가능한 아이디입니다." if available else "이미 사용 중인 아이디입니다.",
    )


@app.post("/signup", response_model=SignupResponse)
async def signup(req: SignupRequest, db: AsyncSession = Depends(get_db)) -> SignupResponse:
    """회원가입 — uvicorn 터미널에 입력 정보 로그."""
    role = req.role if req.role in ("user", "admin", "coach") else "user"
    logger.info(
        "[회원가입] 아이디=%s | 이메일=%s | 닉네임=%s | role=%s",
        req.userId,
        req.email,
        req.nickname,
        role,
    )

    user_schema = UserSchema(
        userId=req.userId,
        password=req.password,
        email=req.email,
        nickname=req.nickname,
        role=role,
    )

    try:
        user_controller = UserService(db)
        await user_controller.save_user(user_schema)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="이미 사용 중인 아이디 또는 이메일입니다.",
        ) from e

    return SignupResponse(
        message="회원가입 요청이 접수되었습니다.",
        userId=req.userId,
        email=req.email,
        nickname=req.nickname,
        role=role,
    )


@app.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)) -> LoginResponse:
    """로그인 — uvicorn 터미널에 입력 정보 로그."""
    logger.info(
        "[로그인] 아이디=%s | 비밀번호=%s ",
        req.userId,
        req.password,
    )

    login_schema = LoginSchema(
        userId=req.userId,
        password=req.password,
    )

    user_controller = UserService(db)
    try:
        await user_controller.login_user(login_schema)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    role = await user_controller.get_user_role(req.userId)

    return LoginResponse(
        message="로그인 요청이 접수되었습니다.",
        userId=req.userId,
        role=role,
    )


@app.get("/mypage/profile", response_model=MyPageProfileResponse)
async def get_mypage_profile(userId: str, db: AsyncSession = Depends(get_db)) -> MyPageProfileResponse:
    """마이페이지 프로필 조회 — Neon `user_information` 테이블."""
    user_id = userId.strip()
    if not user_id:
        raise HTTPException(status_code=400, detail="userId가 필요합니다.")

    user_controller = UserService(db)
    profile = await user_controller.get_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return profile


@app.put("/mypage/profile", response_model=MyPageProfileResponse)
async def save_mypage_profile(
    req: MyPageProfileSchema, db: AsyncSession = Depends(get_db)
) -> MyPageProfileResponse:
    """마이페이지 프로필 저장 — Neon `user_information` INSERT/UPDATE."""
    try:
        user_controller = UserService(db)
        await user_controller.save_profile(req)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    profile = await user_controller.get_profile(req.userId)
    if profile is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    profile.message = "마이페이지 정보가 저장되었습니다."
    return profile


class ScheduleAccessStatusResponse(BaseModel):
    configured: bool


class ScheduleAccessVerifyRequest(BaseModel):
    userId: str = Field(min_length=1)
    password: str = Field(min_length=1)


class ScheduleAccessAdmittedResponse(BaseModel):
    admitted: bool


class ScheduleAccessVerifyResponse(BaseModel):
    ok: bool = True


class ScheduleAccessPasswordRequest(BaseModel):
    userId: str = Field(min_length=1)
    password: str = Field(min_length=4)


class ScheduleAccessPasswordResponse(BaseModel):
    message: str = "스케줄 접근 암호가 설정되었습니다."


@app.get("/schedule/access/status", response_model=ScheduleAccessStatusResponse)
async def schedule_access_status(db: AsyncSession = Depends(get_db)) -> ScheduleAccessStatusResponse:
    service = ScheduleAccessService(db)
    configured = await service.is_configured()
    return ScheduleAccessStatusResponse(configured=configured)


@app.get("/schedule/access/admitted", response_model=ScheduleAccessAdmittedResponse)
async def schedule_access_admitted(
    userId: str, db: AsyncSession = Depends(get_db)
) -> ScheduleAccessAdmittedResponse:
    member_id = userId.strip()
    if not member_id:
        raise HTTPException(status_code=400, detail="userId가 필요합니다.")
    service = ScheduleAccessService(db)
    admitted = await service.is_admitted(member_id)
    return ScheduleAccessAdmittedResponse(admitted=admitted)


@app.post("/schedule/access/verify", response_model=ScheduleAccessVerifyResponse)
async def schedule_access_verify(
    req: ScheduleAccessVerifyRequest, db: AsyncSession = Depends(get_db)
) -> ScheduleAccessVerifyResponse:
    service = ScheduleAccessService(db)
    try:
        await service.verify_and_grant(req.userId.strip(), req.password)
    except ValueError as e:
        msg = str(e)
        status = 401 if "올바르지 않습니다" in msg else 400
        raise HTTPException(status_code=status, detail=msg) from e
    return ScheduleAccessVerifyResponse()


class ScheduleInviteCreateRequest(BaseModel):
    userId: str = Field(min_length=1)


class ScheduleInviteCreateResponse(BaseModel):
    code: str
    expiresAt: str


class ScheduleInviteRedeemRequest(BaseModel):
    userId: str = Field(min_length=1)
    code: str = Field(min_length=1)


class ScheduleInviteRedeemResponse(BaseModel):
    ok: bool = True


@app.post("/schedule/invites", response_model=ScheduleInviteCreateResponse)
async def schedule_invite_create(
    req: ScheduleInviteCreateRequest, db: AsyncSession = Depends(get_db)
) -> ScheduleInviteCreateResponse:
    service = ScheduleAccessService(db)
    try:
        payload = await service.create_invite_code(req.userId.strip())
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    return ScheduleInviteCreateResponse(**payload)


@app.post("/schedule/invites/redeem", response_model=ScheduleInviteRedeemResponse)
async def schedule_invite_redeem(
    req: ScheduleInviteRedeemRequest, db: AsyncSession = Depends(get_db)
) -> ScheduleInviteRedeemResponse:
    service = ScheduleAccessService(db)
    try:
        await service.redeem_invite_code(req.userId.strip(), req.code)
    except ValueError as e:
        msg = str(e)
        status = 401 if "올바르지 않" in msg or "만료" in msg else 400
        raise HTTPException(status_code=status, detail=msg) from e
    return ScheduleInviteRedeemResponse()


@app.put("/schedule/access/password", response_model=ScheduleAccessPasswordResponse)
async def schedule_access_set_password(
    req: ScheduleAccessPasswordRequest, db: AsyncSession = Depends(get_db)
) -> ScheduleAccessPasswordResponse:
    service = ScheduleAccessService(db)
    try:
        await service.set_password(req.userId.strip(), req.password)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    return ScheduleAccessPasswordResponse()


class ScheduleMemberItem(BaseModel):
    userId: str
    nickname: str


class ScheduleMembersResponse(BaseModel):
    members: list[ScheduleMemberItem]


@app.get("/schedule/members", response_model=ScheduleMembersResponse)
async def schedule_members(userId: str, db: AsyncSession = Depends(get_db)) -> ScheduleMembersResponse:
    """코치·관리자용 — 접근 암호를 입력한 회원만 (스케줄 탭)."""
    coach_id = userId.strip()
    if not coach_id:
        raise HTTPException(status_code=400, detail="userId가 필요합니다.")
    service = ScheduleAccessService(db)
    try:
        rows = await service.list_admitted_members_for_coach(coach_id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    return ScheduleMembersResponse(
        members=[ScheduleMemberItem(userId=r["userId"], nickname=r["nickname"]) for r in rows],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)