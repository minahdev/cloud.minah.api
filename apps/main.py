import logging
from typing import Literal

import httpx
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.db_health_adapter import DatabaseHealthAdapter
from deps import get_db, inject_keymaker
from matrix.app.keymaker import Keymaker, is_gemini_quota_error
from titanic.app.james_controller import JamesController
from doro.app.doro_diretor import Diretor
from chat_mirror import get_last_chat, record_chat
from weather.app.weather_controller import WeatherController
from secom.app.schemas.user_schema import UserSchema
from secom.app.controllers.user_controller import UserController

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
    force=True,
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Minahdev Cloud Main Page")


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


class SignupResponse(BaseModel):
    message: str
    userId: str
    email: str
    nickname: str
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

#타이타닉 데이터
@app.get("/titanic/data")
def read_titanic_data():
    james = JamesController()
    df = james.get_data_titanic()
    return df.to_dict(orient="records")


#타이타닉 전체 승객 수
@app.get("/titanic/count")
def read_titanic_count():
    james = JamesController()
    total_passengers = james.titanic_count()
    return {"total_passengers": total_passengers}


#타이타닉 생존자 수
@app.get("/titanic/count/survived")
def read_titanic_survived():
    james = JamesController()
    survived_passengers = james.titanic_survived()
    return {"survived_passengers": survived_passengers}


#타이타닉 사망자 수
@app.get("/titanic/count/dead")
def read_titanic_dead():
    james = JamesController()
    dead_passengers = james.titanic_dead()
    return {"dead_passengers": dead_passengers}



#타이타닉 결정트리 모델명, 정확도 표시
@app.get("/titanic/model")
def read_titanic_tree():
    james = JamesController()
    model_name = james.current_model_name()
    accuracy = james.current_model_accuracy()
    return {"model_name": model_name, "accuracy": accuracy}




@app.get("/doro/data")
def read_doro_data():
    diretor = Diretor()
    df = diretor.get_data_doro()
    return df.to_dict(orient="records")


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DatabaseHealthAdapter.server_time_payload(db)



@app.post("/signup", response_model=SignupResponse)
async def signup(req: SignupRequest) -> SignupResponse:
    """회원가입 — uvicorn 터미널에 입력 정보 로그."""
    logger.info(
        "[회원가입] 아이디=%s | 비밀번호=%s | 이메일=%s | 닉네임=%s",
        req.userId,
        req.password,
        req.email,
        req.nickname,
    )


    #프론트엔드에서 가져온 데이터를 스키마에 담아서 DB로 보내는 코드
    user_schema = UserSchema(
        userId=req.userId,
        password=req.password,
        email=req.email,
        nickname=req.nickname,
        role="user",
    )

    user_controller = UserController()
    user_controller.save_user(user_schema)


    return SignupResponse(
        message="회원가입 요청이 접수되었습니다.",
        userId=req.userId,
        email=req.email,
        nickname=req.nickname,
        role="user",
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)