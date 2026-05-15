from typing import Literal

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.db_health_adapter import DatabaseHealthAdapter
from deps import get_db, inject_keymaker
from matrix.app.keymaker import Keymaker, is_gemini_quota_error
from titanic.app.james_controller import JamesController
from doro.app.doro_diretor import Diretor
from chat_html import render_chat_page
from chat_mirror import get_last_chat, record_chat
from weather.app.weather_controller import WeatherController

app = FastAPI(title="Minahdev Cloud Main Page")


def _wants_html(request: Request, format_param: str | None) -> bool:
    if format_param == "json":
        return False
    if format_param == "html":
        return True
    accept = request.headers.get("accept", "").lower()
    return "text/html" in accept and not accept.strip().startswith("application/json")


class ChatMessage(BaseModel):
    role: Literal["user", "model"]
    text: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1)


class ChatResponse(BaseModel):
    text: str


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


@app.get("/chat/last")
def chat_last():
    """프론트 POST /chat 이후 저장된 최근 질문·답변 (JSON)."""
    snap = get_last_chat()
    if snap is None:
        return {"user_text": None, "model_text": None, "model_name": None, "updated_at": None}
    return snap.to_dict()


@app.get("/chat")
def chat_info(request: Request, format: str | None = None):
    """
    브라우저: 프론트 Gemini 채팅과 동기화된 최근 Q&A HTML.
    API: JSON 안내 또는 ?format=json 시 최근 대화 스냅샷.
    """
    snap = get_last_chat()
    if _wants_html(request, format):
        return HTMLResponse(render_chat_page(snap))

    if snap is not None:
        return {
            "message": "최근 Gemini 대화 (프론트 채팅과 동기화)",
            "last": snap.to_dict(),
            "view_html": "/chat (브라우저)",
            "poll": "/chat/last",
        }

    return {
        "message": "아직 대화가 없습니다. 프론트(3000) 홈 Gemini 채팅에서 질문하세요.",
        "method": "POST",
        "body_example": {"messages": [{"role": "user", "text": "한국의 수도는 어디인가요?"}]},
        "view_html": "/chat (브라우저)",
        "poll": "/chat/last",
    }


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
def read_root(request: Request, format: str | None = None):
    if _wants_html(request, format):
        return HTMLResponse(render_chat_page(get_last_chat()))
    return {
        "message": "FastAPI 메인페이지",
        "docs": "/docs",
        "chat_mirror": "/chat",
        "chat_last": "/chat/last",
    }

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)