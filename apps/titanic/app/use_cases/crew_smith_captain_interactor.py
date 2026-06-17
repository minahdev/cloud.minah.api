from __future__ import annotations
from typing import Any

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    SmithCaptainSchema,
    ChatSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainQuery
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort

import logging

logger = logging.getLogger(__name__)

# Jack키 → Rose키 매핑 (두 전략 맵의 키가 다른 항목만)
_JACK_TO_ROSE_KEY: dict[str, str] = {
    "random_forest":      "randomforest",
    "logistic_regression":"logisticregression",
    "decision_tree":      "decisiontree",
    "naive_bayes":        "naivebayes",
    "kmeans_pca":         "pca_kmeans",
}

_EMBARKED_MAP = {"C": 0.0, "Q": 1.0, "S": 2.0}


def _extract_xy(df: pd.DataFrame) -> tuple[list[list[float]], list[int]]:
    """Walter train_set DataFrame → (X, y) — Rose SurvivalModelStrategy 학습용."""
    X: list[list[float]] = []
    y: list[int] = []
    for _, row in df.iterrows():
        try:
            survived = int(row.get("survived", 0))
        except (ValueError, TypeError):
            continue
        sex = 1.0 if str(row.get("gender", "")).lower() == "female" else 0.0
        features = [
            float(row.get("pclass") or 3),
            sex,
            float(row.get("age") or 29.7),
            float(row.get("sib_sp") or 0),
            float(row.get("parch") or 0),
            float(row.get("fare") or 32.2),
            _EMBARKED_MAP.get(str(row.get("embarked") or ""), 2.0),
        ]
        X.append(features)
        y.append(survived)
    return X, y


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
            self,
            repository: SmithCaptainPort,
            rose: RoseModelUseCase,
            jack: JackTrainerUseCase,
            cal: CalTesterUseCase,
            walter: WalterRoasterUseCase,
            andrews: AndrewsArchitectUseCase,
        ):
        self._repository = repository
        self.rose = rose
        self.jack = jack
        self.cal = cal
        self.walter = walter
        self.andrews = andrews

    async def chat(self, schema: ChatSchema) -> SmithCaptainResponse:
        logger.info(f"[SmithCaptainInteractor] chat 진입 | messages={schema.messages}")

        # 1. Walter에서 train/test 데이터 수집
        train_df = await self.walter.get_train_set()
        test_df  = await self.walter.get_test_set()

        # 2. Jack이 10개 모델 학습
        train_result = await self.jack.train_model(train_df)

        # 3. Cal이 채점 → 챔피언 선정 (label 있는 train_df로 평가)
        test_result = await self.cal.test_model({
            "df": train_df,
            "trained_strategies": train_result["trained_strategies"],
        })

        champion     = test_result.get("champion") or {}
        champion_key = champion.get("key", "random_forest")
        accuracy     = champion.get("accuracy", 0.0)

        # 4. 로즈에게 챔피언 알고리즘(SurvivalModelStrategy) 장착
        from titanic.app.use_cases.passenger_rose_model_interactor import build_all_strategies
        rose_key = _JACK_TO_ROSE_KEY.get(champion_key, champion_key)
        rose_strategies = build_all_strategies()
        if rose_key in rose_strategies:
            champion_strategy = rose_strategies[rose_key]()
            X_train, y_train = _extract_xy(train_df)
            champion_strategy.fit(X_train, y_train)
            self.rose.set_strategy(champion_strategy)
            logger.info(f"[SmithCaptainInteractor] Rose에 {rose_key} 장착 완료")

        # 5. Andrews가 질문 의도 분석
        message_text = next(
            (m.get("content", "") for m in reversed(schema.messages)
             if isinstance(m, dict) and m.get("role") == "user"),
            "",
        )
        question = self.andrews.analyze_intent(message_text)
        intent   = question.get("intent", "UNKNOWN")

        # 6. 의도에 따라 응답 구성
        import re
        suffix = f"\n({champion_key} 모델 정확도 {accuracy:.1%})"

        if intent == "STATISTICS":
            total = len(train_df) + len(test_df)
            survived_series = pd.to_numeric(train_df["survived"], errors="coerce").dropna()
            survival_rate = survived_series.mean() if len(survived_series) > 0 else 0.0
            text = f"총 {total}명이 탑승했으며, 생존율은 {survival_rate:.1%}입니다." + suffix

        elif intent == "SURVIVAL_PREDICT":
            age_match = re.search(r"(\d+)\s*대", message_text)
            df = train_df.copy()
            df["age"] = pd.to_numeric(df["age"], errors="coerce")
            df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
            df = df.dropna(subset=["age", "survived"])
            if age_match:
                decade = int(age_match.group(1))
                group = df[(df["age"] >= decade) & (df["age"] < decade + 10)]
                if len(group) > 0:
                    text = f"{decade}대 승객 {len(group)}명의 생존율은 {group['survived'].mean():.1%}입니다." + suffix
                else:
                    text = f"{decade}대 승객 데이터가 충분하지 않습니다." + suffix
            else:
                rate = df["survived"].mean() if len(df) > 0 else 0.0
                text = f"전체 생존율은 {rate:.1%}입니다." + suffix

        elif intent == "PASSENGER_SEARCH":
            all_df = pd.concat([train_df, test_df], ignore_index=True)
            keywords = question.get("keywords", [])
            found = all_df[all_df["name"].str.contains("|".join(keywords), case=False, na=False)] if keywords else pd.DataFrame()
            if len(found) > 0:
                lines = []
                for _, row in found.head(5).iterrows():
                    survived_val = row.get("survived", "")
                    status = "생존" if str(survived_val) == "1" else ("사망" if str(survived_val) == "0" else "미확인")
                    lines.append(f"- {row.get('name', '?')} ({row.get('gender', '?')}, {row.get('age', '?')}세) → {status}")
                text = "검색된 승객:\n" + "\n".join(lines) + suffix
            else:
                text = "해당 승객을 찾지 못했습니다." + suffix

        elif intent == "MODEL_TRAIN":
            ranking = test_result.get("ranking", [])
            lines = [
                f"{r['rank']}위 {r['name']} — 정확도 {r['accuracy']:.1%}"
                for r in ranking
                if r.get("accuracy") is not None
            ]
            text = "모델 성능 순위:\n" + "\n".join(lines)

        else:
            text = f"죄송합니다, 그 질문은 아직 답변하기 어렵습니다." + suffix

        logger.info(
            f"[SmithCaptainInteractor] chat 완료 | intent={intent} "
            f"champion={champion_key} accuracy={accuracy}"
        )
        return SmithCaptainResponse(text=text)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        return self._repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))
