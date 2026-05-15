import os
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

# backend/apps/matrix/app/keymaker.py → backend/
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent.parent
_ENV_PATH = _BACKEND_DIR / ".env"

WEATHER_API_KEY_ENV = "WEATHER_API_KEY"

# 무료 한도가 남아 있는 모델 우선 (2.0-flash-lite 등은 한도 0인 계정이 많음)
_DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
_DEFAULT_FALLBACK_MODELS = (
    "gemini-2.5-flash-lite,gemini-flash-lite-latest,gemini-2.5-flash"
)

_CHAT_SYSTEM_INSTRUCTION = """당신은 Pace 헬스케어 포트폴리오 사이트의 AI 어시스턴트입니다.
반드시 한국어로 답변하세요.

가독성 규칙:
- 문단은 2~3문장으로 짧게 나누고, 문단 사이에 빈 줄을 넣으세요.
- 목록은 `-` 또는 `1.` 번호 목록을 사용하세요.
- 강조는 **굵게**만 사용하세요.
- 긴 글은 ## 소제목으로 섹션을 나누세요.
- 불필요한 반복·장황한 서론은 피하고 핵심만 담으세요.
"""


def load_app_env() -> None:
    """backend/.env 를 한 번 로드합니다. idempotent."""
    load_dotenv(_ENV_PATH)


load_app_env()


def is_gemini_quota_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "429" in str(exc) or "quota" in msg or "resource exhausted" in msg


class Keymaker:
    """앱 전역 API 키·클라이언트 설정을 한 곳에서 관리합니다."""

    def __init__(self) -> None:
        self.gemini_api_key: str = (os.getenv("GEMINI_API_KEY") or "").strip()
        self.weather_api_key: str = (os.getenv(WEATHER_API_KEY_ENV) or "").strip()
        self.gemini_model_name: str = (
            os.getenv("GEMINI_MODEL") or _DEFAULT_GEMINI_MODEL
        ).strip()
        self._gemini_model: genai.GenerativeModel | None
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self._gemini_model = self._create_model(self.gemini_model_name)
        else:
            self._gemini_model = None

    def _create_model(self, model_name: str) -> genai.GenerativeModel:
        return genai.GenerativeModel(
            model_name,
            system_instruction=_CHAT_SYSTEM_INSTRUCTION,
        )

    def gemini_model_candidates(self) -> list[str]:
        """우선 모델 + fallback 목록 (중복 제거)."""
        extra = os.getenv("GEMINI_MODEL_FALLBACKS", _DEFAULT_FALLBACK_MODELS)
        fallbacks = [m.strip() for m in extra.split(",") if m.strip()]
        seen: set[str] = set()
        ordered: list[str] = []
        for name in [self.gemini_model_name, *fallbacks]:
            if name and name not in seen:
                seen.add(name)
                ordered.append(name)
        return ordered

    def send_chat(self, history: list[dict], user_text: str) -> tuple[str, str]:
        """
        Gemini 채팅 전송. 할당량(429)이면 다음 모델로 자동 재시도.
        Returns: (reply_text, model_name_used)
        """
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY가 설정되어 있지 않습니다.")

        genai.configure(api_key=self.gemini_api_key)
        quota_models: list[str] = []
        last_error: BaseException | None = None

        for model_name in self.gemini_model_candidates():
            try:
                model = self._create_model(model_name)
                session = model.start_chat(history=history)
                response = session.send_message(user_text)
                text = (response.text or "").strip()
                if not text:
                    continue
                self.gemini_model_name = model_name
                self._gemini_model = model
                return text, model_name
            except Exception as e:
                last_error = e
                if is_gemini_quota_error(e):
                    quota_models.append(model_name)
                    continue
                raise

        detail = (
            "Gemini API 무료 할당량을 모두 소진했거나, 사용 중인 모델에 한도가 없습니다. "
            "잠시 후 다시 시도하거나 https://aistudio.google.com 에서 API 키·사용량을 확인하세요."
        )
        if quota_models:
            detail += f" (한도 초과로 건너뜀: {', '.join(quota_models)})"
        raise RuntimeError(detail) from last_error

    @property
    def gemini_model(self) -> genai.GenerativeModel | None:
        return self._gemini_model

    @property
    def has_weather_api_key(self) -> bool:
        return bool(self.weather_api_key)

    def get_weather_api_key(self) -> str:
        """날씨 API 호출용 키. 없으면 ValueError."""
        if not self.weather_api_key:
            raise ValueError(
                f"'.env'에 {WEATHER_API_KEY_ENV}를 설정하세요."
            )
        return self.weather_api_key

    @property
    def database_url(self) -> str | None:
        raw = os.getenv("DATABASE_URL")
        if not raw or not str(raw).strip():
            return None
        return str(raw).strip()


_keymaker: Keymaker | None = None


def get_keymaker() -> Keymaker:
    """앱 전역 단일 Keymaker 인스턴스를 반환합니다."""
    global _keymaker
    if _keymaker is None:
        _keymaker = Keymaker()
    return _keymaker
