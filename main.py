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

import base64
import hashlib
import hmac
import os
import secrets
import httpx
from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

_basic_security = HTTPBasic()
_SESSION_COOKIE = "_api_sess"
_SESSION_VALUE = "ok"


def _session_secret() -> bytes:
    return os.getenv("SESSION_SECRET", "changeme").encode()


def _make_cookie() -> str:
    sig = hmac.new(_session_secret(), _SESSION_VALUE.encode(), hashlib.sha256).hexdigest()
    return f"{_SESSION_VALUE}.{sig}"


def _valid_cookie(value: str) -> bool:
    try:
        payload, sig = value.rsplit(".", 1)
        expected = hmac.new(_session_secret(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected) and payload == _SESSION_VALUE
    except Exception:
        return False


def _check_basic_auth(auth_header: str) -> bool:
    if not auth_header.startswith("Basic "):
        return False
    expected_user = os.getenv("API_USERNAME", "")
    expected_pass = os.getenv("API_PASSWORD", "")
    if not expected_user:
        return False
    try:
        decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
        username, _, password = decoded.partition(":")
        return (
            secrets.compare_digest(username.encode(), expected_user.encode())
            and secrets.compare_digest(password.encode(), expected_pass.encode())
        )
    except Exception:
        return False


_LOGIN_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Minahdev API — 로그인</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#0f0f0f;font-family:system-ui,sans-serif}}
.card{{background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:40px;width:340px}}
h1{{color:#fff;font-size:18px;margin-bottom:8px}}
p{{color:#888;font-size:13px;margin-bottom:28px}}
label{{display:block;color:#aaa;font-size:12px;margin-bottom:6px}}
input{{width:100%;padding:10px 12px;background:#111;border:1px solid #333;border-radius:8px;color:#fff;font-size:14px;margin-bottom:16px;outline:none}}
input:focus{{border-color:#555}}
button{{width:100%;padding:11px;background:#fff;color:#000;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer}}
button:hover{{background:#e0e0e0}}
.error{{color:#f87171;font-size:13px;margin-bottom:16px;display:{error_display}}}
</style>
</head>
<body>
<div class="card">
  <h1>Minahdev API</h1>
  <p>관리자 전용 접근입니다.</p>
  <div class="error">{error_msg}</div>
  <form method="post" action="/login">
    <label>아이디</label>
    <input type="text" name="username" autofocus autocomplete="username">
    <label>비밀번호</label>
    <input type="password" name="password" autocomplete="current-password">
    <button type="submit">로그인</button>
  </form>
</div>
</body>
</html>"""


class _AuthMiddleware(BaseHTTPMiddleware):
    _SKIP = {"/login", "/logout"}

    async def dispatch(self, request: Request, call_next):
        if not os.getenv("API_USERNAME"):
            return await call_next(request)
        if request.url.path in self._SKIP:
            return await call_next(request)

        # Vercel 서버 사이드 호출 — Basic Auth 헤더
        if _check_basic_auth(request.headers.get("Authorization", "")):
            return await call_next(request)

        # 브라우저 — 세션 쿠키
        if _valid_cookie(request.cookies.get(_SESSION_COOKIE, "")):
            return await call_next(request)

        # 브라우저면 로그인 페이지로, API 호출이면 401
        accept = request.headers.get("Accept", "")
        if "text/html" in accept:
            return RedirectResponse(url="/login", status_code=302)
        return Response("Unauthorized", status_code=401)
from apps.deps import inject_keymaker
from core.matrix.secret_manager import Keymaker, is_gemini_quota_error
from chat_mirror import get_last_chat, record_chat
from weather.app.weather_controller import WeatherController
from core.matrix.database_manager import (
    create_database_tables,
    create_database_tables_windows_threadsafe,
    get_db,
)
from users.adapter.inbound.api.schemas.mypage_schema import (
    MyPageProfileResponse,
    MyPageProfileSchema,
)
from users.adapter.inbound.api.schemas.user_schema import LoginSchema, UserSchema
from users.adapter.outbound.pg.login_pg_repository import LoginPgRepository
from users.adapter.outbound.pg.signup_pg_repository import SignupPgRepository
from users.adapter.outbound.pg.user_pg_information_repository import UserInformationRepository
from users.adapter.outbound.pg.user_pg_repository import UserPgRepository
from users.app.use_cases.login_interactor import LoginInteractor
from users.app.use_cases.mypage_interactor import MyPageInteractor
from users.app.ports.input.schedule_access_use_case import ScheduleAccessUseCase
from users.dependencies.schedule_access_provider import get_schedule_access_use_case
from users.app.use_cases.signup_interactor import SignupInteractor
from users.app.use_cases.user_interactor import UserService
from inbody.community_media import get_community_media_storage
from inbody.router import router as inbody_router
from titanic.adapter.inbound.api import titanic_router
from silicon_valley.adapter.inbound.api import silicon_valley_router
from comm_agent.adapter.inbound.api import comm_agent_router
from spam_filter.adapter.inbound.api import spam_filter_router
from star_craft.adapter.inbound.api import star_craft_router
from vision.adapter.inbound.api.v1.vision_router import vision_router

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


app = FastAPI(title="Minahdev Cloud Main Page", lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(_AuthMiddleware)


@app.get("/login", include_in_schema=False)
def login_page() -> HTMLResponse:
    html = _LOGIN_HTML.format(error_display="none", error_msg="")
    return HTMLResponse(html)


@app.post("/login", include_in_schema=False)
def login_submit(username: str = Form(...), password: str = Form(...)):
    expected_user = os.getenv("API_USERNAME", "")
    expected_pass = os.getenv("API_PASSWORD", "")
    ok = (
        bool(expected_user)
        and secrets.compare_digest(username.encode(), expected_user.encode())
        and secrets.compare_digest(password.encode(), expected_pass.encode())
    )
    if not ok:
        html = _LOGIN_HTML.format(error_display="block", error_msg="아이디 또는 비밀번호가 올바르지 않습니다.")
        return HTMLResponse(html, status_code=401)
    response = RedirectResponse(url="/docs", status_code=302)
    response.set_cookie(_SESSION_COOKIE, _make_cookie(), httponly=True, samesite="lax")
    return response


@app.get("/logout", include_in_schema=False)
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(_SESSION_COOKIE)
    return response


@app.get("/docs", include_in_schema=False)
def custom_docs() -> HTMLResponse:
    logout_btn = '<a href="/logout" style="position:fixed;top:12px;right:16px;padding:6px 14px;background:#ef4444;color:#fff;border-radius:6px;font-size:13px;text-decoration:none;z-index:9999">로그아웃</a>'
    html = get_swagger_ui_html(openapi_url="/openapi.json", title="Minahdev Cloud Main Page").body.decode()
    html = html.replace("</body>", f"{logout_btn}</body>")
    return HTMLResponse(html)


@app.get("/openapi.json", include_in_schema=False)
def custom_openapi() -> JSONResponse:
    return JSONResponse(get_openapi(title=app.title, version=app.version, routes=app.routes))


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


app.include_router(inbody_router)
app.include_router(titanic_router, prefix="/api")
app.include_router(silicon_valley_router, prefix="/api")
app.include_router(comm_agent_router, prefix="/api")
app.include_router(spam_filter_router, prefix="/api")
app.include_router(star_craft_router, prefix="/api")
app.include_router(vision_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}



@app.get("/signup/check-userid", response_model=UserIdCheckResponse)
async def check_signup_user_id(userId: str, db: AsyncSession = Depends(get_db)) -> UserIdCheckResponse:
    """회원가입 전 아이디 중복 확인."""
    user_id = userId.strip()
    if not user_id:
        raise HTTPException(status_code=400, detail="userId가 필요합니다.")

    user_controller = SignupInteractor(repository=SignupPgRepository(session=db))
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
        user_controller = SignupInteractor(repository=SignupPgRepository(session=db))
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
    logger.info("[로그인] 아이디=%s", req.userId)

    login_schema = LoginSchema(
        userId=req.userId,
        password=req.password,
    )

    try:
        await LoginInteractor(repository=LoginPgRepository(session=db)).login_user(login_schema)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    role = await UserService(repository=UserPgRepository(session=db)).get_user_role(req.userId)

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

    user_controller = MyPageInteractor(repository=UserInformationRepository(session=db))
    profile = await user_controller.get_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return profile


@app.put("/mypage/profile", response_model=MyPageProfileResponse)
async def save_mypage_profile(
    req: MyPageProfileSchema, db: AsyncSession = Depends(get_db)
) -> MyPageProfileResponse:
    """마이페이지 프로필 저장 — Neon `user_information` INSERT/UPDATE."""
    user_controller = MyPageInteractor(repository=UserInformationRepository(session=db))
    try:
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
async def schedule_access_status(service: ScheduleAccessUseCase = Depends(get_schedule_access_use_case)) -> ScheduleAccessStatusResponse:
    configured = await service.is_configured()
    return ScheduleAccessStatusResponse(configured=configured)


@app.get("/schedule/access/admitted", response_model=ScheduleAccessAdmittedResponse)
async def schedule_access_admitted(
    userId: str, service: ScheduleAccessUseCase = Depends(get_schedule_access_use_case)
) -> ScheduleAccessAdmittedResponse:
    member_id = userId.strip()
    if not member_id:
        raise HTTPException(status_code=400, detail="userId가 필요합니다.")
    admitted = await service.is_admitted(member_id)
    return ScheduleAccessAdmittedResponse(admitted=admitted)


@app.post("/schedule/access/verify", response_model=ScheduleAccessVerifyResponse)
async def schedule_access_verify(
    req: ScheduleAccessVerifyRequest, service: ScheduleAccessUseCase = Depends(get_schedule_access_use_case)
) -> ScheduleAccessVerifyResponse:
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
    req: ScheduleInviteCreateRequest, service: ScheduleAccessUseCase = Depends(get_schedule_access_use_case)
) -> ScheduleInviteCreateResponse:
    try:
        payload = await service.create_invite_code(req.userId.strip())
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    return ScheduleInviteCreateResponse(**payload)


@app.post("/schedule/invites/redeem", response_model=ScheduleInviteRedeemResponse)
async def schedule_invite_redeem(
    req: ScheduleInviteRedeemRequest, service: ScheduleAccessUseCase = Depends(get_schedule_access_use_case)
) -> ScheduleInviteRedeemResponse:
    try:
        await service.redeem_invite_code(req.userId.strip(), req.code)
    except ValueError as e:
        msg = str(e)
        status = 401 if "올바르지 않" in msg or "만료" in msg else 400
        raise HTTPException(status_code=status, detail=msg) from e
    return ScheduleInviteRedeemResponse()


@app.put("/schedule/access/password", response_model=ScheduleAccessPasswordResponse)
async def schedule_access_set_password(
    req: ScheduleAccessPasswordRequest, service: ScheduleAccessUseCase = Depends(get_schedule_access_use_case)
) -> ScheduleAccessPasswordResponse:
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
async def schedule_members(userId: str, service: ScheduleAccessUseCase = Depends(get_schedule_access_use_case)) -> ScheduleMembersResponse:
    """코치·관리자용 — 접근 암호를 입력한 회원만 (스케줄 탭)."""
    coach_id = userId.strip()
    if not coach_id:
        raise HTTPException(status_code=400, detail="userId가 필요합니다.")
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