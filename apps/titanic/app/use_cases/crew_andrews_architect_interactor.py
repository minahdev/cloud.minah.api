from __future__ import annotations
from typing import Any
import re

import pandas as pd
from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import (
    AndrewsArchitectSchema,
)
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse, AndrewsArchitectQuery
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_port import AndrewsArchitectPort
from titanic.domain.constants.intent_map import INTENT_MAP

import logging

logger = logging.getLogger(__name__)

class AndrewsArchitectInteractor(AndrewsArchitectUseCase):

    def __init__(self, repository: AndrewsArchitectPort):
        self.repository = repository
        self.kiwi = Kiwi()

    def analyze_intent(self, messages: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 프론트 질문의 의도를 파악하는 메소드

        반환값:
            intent   : 감지된 의도 (SURVIVAL_PREDICT / STATISTICS / PASSENGER_SEARCH / MODEL_TRAIN / UNKNOWN)
            keywords : 분석에 사용된 핵심 형태소 목록
            scores   : 의도별 매칭 점수
            tokens   : Kiwi가 분석한 전체 (형태소, 품사) 쌍 목록
        '''
        # 명사(NN*), 동사 어간(VV/VA), 파생어근(XR)만 의도 판별에 사용
        tokens = self.kiwi.tokenize(messages)
        keywords = [t.form for t in tokens if t.tag.startswith(("NN", "VV", "VA", "XR"))]

        scores: dict[str, int] = {intent: 0 for intent in INTENT_MAP}
        for keyword in keywords:
            for intent, kw_set in INTENT_MAP.items():
                if keyword in kw_set:
                    scores[intent] += 1

        best_intent = max(scores, key=lambda k: scores[k])
        intent = best_intent if scores[best_intent] > 0 else "UNKNOWN"

        logger.info
        (
            f"[AndrewsArchitectInteractor] analyze_intent | messages={messages!r} "
            f"intent={intent} scores={scores}"
        )
        return {
            "intent": intent,
            "keywords": keywords,
            "scores": scores,
            "tokens": [(t.form, str(t.tag)) for t in tokens],
        }

    def answer(self, question: str, train_set: pd.DataFrame, champion_strategy=None) -> str:
        '''의도 분석 결과에 따라 자연어 답변을 생성한다.'''
        intent_result = self.analyze_intent(question)
        intent = intent_result["intent"]

        if intent == "SURVIVAL_PREDICT":
            return self._answer_survival_predict(question, train_set, champion_strategy)
        elif intent == "STATISTICS":
            return self._answer_statistics(train_set)
        elif intent == "AGE_EXTREME":
            return self._answer_age_extreme(question, train_set)
        elif intent == "FAMILY_ANALYSIS":
            return self._answer_family_analysis(question, train_set)
        elif intent == "FARE_ANALYSIS":
            return self._answer_fare_analysis(question, train_set)
        elif intent == "PCLASS_SURVIVAL":
            return self._answer_pclass_survival(train_set)
        elif intent == "EMBARKATION":
            return self._answer_embarkation(train_set)
        elif intent == "PASSENGER_SEARCH":
            return self._answer_passenger_search(question, train_set)
        elif intent == "MODEL_TRAIN":
            return "현재 질문마다 10개 ML 모델을 자동으로 훈련하고 있습니다. 별도 훈련 명령은 필요 없습니다."
        else:
            return (
                "안녕하세요! 타이타닉 AI 분석 시스템입니다.\n"
                "다음과 같이 질문해보세요:\n"
                "- '33세 남자라면 살 수 있었을까?'\n"
                "- '최고령 승객은 몇 살이었어?'\n"
                "- '등급별 생존율 차이가 심해?'\n"
                "- '항구별로 생존율이 달랐어?'"
            )

    def _answer_survival_predict(self, question: str, train_set: pd.DataFrame, champion_strategy=None) -> str:
        age_match = re.search(r"(\d+)\s*세", question)
        age = float(age_match.group(1)) if age_match else None

        is_female = any(k in question for k in ["여자", "여성", "female", "woman"])
        is_male   = any(k in question for k in ["남자", "남성", "male", "man"])

        pclass_match = re.search(r"([1-3])\s*등", question)
        pclass = int(pclass_match.group(1)) if pclass_match else None

        # 남녀 비교 질문
        if is_female and is_male:
            return self._answer_gender_survival(train_set)

        # 특정 조건 없음 → 전체 생존율
        if not age and not is_female and not is_male and not pclass:
            df = train_set.copy()
            df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
            rate = df["survived"].mean()
            survived_count = int(df["survived"].sum())
            return f"타이타닉 전체 승객 {len(df)}명 중 {survived_count}명이 생존했습니다. 전체 생존율은 {rate:.1%}입니다."

        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        if is_female:
            df = df[df["gender"] == "female"]
        elif is_male:
            df = df[df["gender"] == "male"]
        if pclass:
            df = df[pd.to_numeric(df["pclass"], errors="coerce") == pclass]

        actual_rate = df["survived"].mean() if len(df) > 0 else None
        gender_str = "여성" if is_female else ("남성" if is_male else "승객")
        age_str = f"{age:.0f}세 " if age else ""

        if champion_strategy is not None:
            feature_vector = [
                1.0 if is_female else 0.0,
                age if age is not None else 29.7,
                0.0,
                0.0,
                float(pclass) if pclass else 3.0,
                32.2,
                1.0,
            ]
            proba = champion_strategy.predict_proba([feature_vector])[0]
            verdict = "살 수 있었을 가능성이 높습니다." if proba >= 0.5 else "안타깝게도 살아남기 어려웠을 것입니다."
            answer = f"{age_str}{gender_str}이라면, {verdict} ML 예측 생존 확률: {proba:.1%}"
            if actual_rate is not None:
                answer += f" (실제 통계: 비슷한 조건 {len(df)}명 중 {actual_rate:.0%} 생존)"
            return answer

        score = 0.0
        if is_female: score += 0.54
        elif is_male: score -= 0.54
        if pclass == 1: score += 0.34
        elif pclass == 3: score -= 0.34
        if age is not None and age < 18: score += 0.10

        verdict = "살 수 있었을 가능성이 높습니다." if score > 0 else "안타깝게도 살아남기 어려웠을 것입니다."
        answer = f"{age_str}{gender_str}이라면, {verdict}"
        if actual_rate is not None:
            answer += f" 실제로 비슷한 조건의 승객 {len(df)}명 중 {actual_rate:.0%}만이 생존했습니다."
        return answer

    def _answer_gender_survival(self, train_set: pd.DataFrame) -> str:
        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        female_rate = df[df["gender"] == "female"]["survived"].mean()
        male_rate   = df[df["gender"] == "male"]["survived"].mean()
        female_count = len(df[df["gender"] == "female"])
        male_count   = len(df[df["gender"] == "male"])
        return (
            f"여성 생존율: {female_rate:.1%} ({female_count}명 중 {int(female_count * female_rate)}명 생존)\n"
            f"남성 생존율: {male_rate:.1%} ({male_count}명 중 {int(male_count * male_rate)}명 생존)\n"
            f"여성의 생존율이 남성보다 {female_rate - male_rate:.1%} 높았습니다. 'Women and children first' 원칙이 실제로 적용되었습니다."
        )

    def _answer_age_extreme(self, question: str, train_set: pd.DataFrame) -> str:
        df = train_set.copy()
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        df = df.dropna(subset=["age"])
        avg_age = df["age"].mean()

        is_youngest = any(k in question for k in ["어린", "최연소", "아기", "어린이"])
        if is_youngest:
            row = df.loc[df["age"].idxmin()]
            survived = "생존" if row["survived"] == 1 else "사망"
            return (
                f"가장 나이가 어린 승객은 {row['age']:.2f}세(약 {row['age']*12:.0f}개월)였으며, {survived}했습니다. "
                f"전체 승객 평균 나이는 {avg_age:.1f}세였습니다."
            )
        else:
            row = df.loc[df["age"].idxmax()]
            survived = "생존" if row["survived"] == 1 else "사망"
            return (
                f"최고령 승객은 {row['age']:.0f}세였으며, {survived}했습니다. "
                f"전체 승객 평균 나이는 {avg_age:.1f}세였습니다."
            )

    def _answer_family_analysis(self, question: str, train_set: pd.DataFrame) -> str:
        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        df["sib_sp"] = pd.to_numeric(df["sib_sp"], errors="coerce").fillna(0)
        df["parch"]  = pd.to_numeric(df["parch"],  errors="coerce").fillna(0)
        df["family_size"] = df["sib_sp"] + df["parch"] + 1

        is_solo  = any(k in question for k in ["혼자", "동반하지", "혼승"])
        is_large = any(k in question for k in ["대가족", "많은 가족"])

        if is_solo:
            solo = df[df["family_size"] == 1]
            pct = len(solo) / len(df) * 100
            return (
                f"혼자 탑승한 승객은 전체 {len(df)}명 중 {len(solo)}명({pct:.1f}%)입니다. "
                f"이들의 생존율은 {solo['survived'].mean():.1%}로, 가족 동반 승객보다 낮았습니다."
            )
        elif is_large:
            large = df[df["family_size"] >= 5]
            return (
                f"5인 이상 대가족 승객은 {len(large)}명이었으며, 생존율은 {large['survived'].mean():.1%}였습니다. "
                f"대가족일수록 함께 이동하기 어려워 생존율이 낮은 경향이 있었습니다."
            )
        else:
            max_size = int(df["family_size"].max())
            solo_rate = df[df["family_size"] == 1]["survived"].mean()
            large_rate = df[df["family_size"] >= 5]["survived"].mean()
            return (
                f"가장 큰 가족 규모는 {max_size}명이었습니다. "
                f"혼자 탑승 생존율: {solo_rate:.1%}, 대가족(5인+) 생존율: {large_rate:.1%}. "
                f"소규모 가족(2~4인)의 생존율이 가장 높았습니다."
            )

    def _answer_fare_analysis(self, question: str, train_set: pd.DataFrame) -> str:
        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        df["fare"] = pd.to_numeric(df["fare"], errors="coerce")

        is_free = any(k in question for k in ["공짜", "0원", "무료"])

        if is_free:
            free = df[df["fare"] == 0]
            return (
                f"요금이 0인 승객은 {len(free)}명이었습니다. "
                f"이들은 주로 승무원이나 특별 초청 탑승자로 추정됩니다. "
                f"생존율은 {free['survived'].mean():.1%}였습니다."
            )
        else:
            max_fare = df["fare"].max()
            avg_fare = df["fare"].mean()
            corr = df[["fare", "survived"]].corr().loc["fare", "survived"]
            return (
                f"가장 비싼 티켓은 £{max_fare:.2f}, 평균 요금은 £{avg_fare:.2f}였습니다. "
                f"요금-생존율 상관계수: {corr:.2f} — 요금이 높을수록 생존율이 높은 경향이 있었습니다."
            )

    def _answer_pclass_survival(self, train_set: pd.DataFrame) -> str:
        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        df["pclass"]   = pd.to_numeric(df["pclass"],   errors="coerce")
        rates  = df.groupby("pclass")["survived"].mean()
        counts = df.groupby("pclass").size()
        return (
            f"등급별 생존율:\n"
            f"  1등석: {rates.get(1, 0):.1%} ({counts.get(1, 0)}명)\n"
            f"  2등석: {rates.get(2, 0):.1%} ({counts.get(2, 0)}명)\n"
            f"  3등석: {rates.get(3, 0):.1%} ({counts.get(3, 0)}명)\n"
            f"등급이 높을수록 구명보트 접근성이 좋아 생존율 차이가 크게 났습니다."
        )

    def _answer_passenger_search(self, question: str, train_set: pd.DataFrame) -> str:
        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")

        is_female = any(k in question for k in ["여자", "여성"])
        is_male   = any(k in question for k in ["남자", "남성"])
        want_survived = any(k in question for k in ["생존", "살아", "살았", "살아남"])

        if is_female or is_male:
            gender = "female" if is_female else "male"
            label  = "여성" if is_female else "남성"
            sub = df[df["gender"] == gender]
            survived_count = int(sub["survived"].sum())
            total_count    = len(sub)
            if want_survived:
                return (
                    f"생존자 중 {label}은 {survived_count}명입니다. "
                    f"전체 {label} 탑승객 {total_count}명 중 {survived_count}명({survived_count/total_count:.1%})이 생존했습니다."
                )
            return (
                f"타이타닉에 탑승한 {label} 승객은 총 {total_count}명이며, "
                f"이 중 {survived_count}명({survived_count/total_count:.1%})이 생존했습니다."
            )

        total    = len(df)
        survived = int(df["survived"].sum())
        return (
            f"타이타닉에 탑승한 승객은 총 {total}명입니다. "
            f"이 중 {survived}명({survived/total:.1%})이 생존했습니다."
        )

    def _answer_embarkation(self, train_set: pd.DataFrame) -> str:
        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        port_map = {"S": "Southampton(영국)", "C": "Cherbourg(프랑스)", "Q": "Queenstown(아일랜드)"}
        rates  = df.groupby("embarked")["survived"].mean().sort_values(ascending=False)
        counts = df.groupby("embarked").size()
        lines = [f"  {port_map.get(p, p)}: {counts.get(p, 0)}명 탑승, 생존율 {r:.1%}" for p, r in rates.items()]
        best = port_map.get(str(rates.idxmax()), str(rates.idxmax()))
        return "항구별 생존율:\n" + "\n".join(lines) + f"\n\n{best} 탑승 승객의 생존율이 가장 높았습니다."

    def _answer_statistics(self, train_set: pd.DataFrame) -> str:
        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        df["gender"]   = df["gender"].map({"female": 1, "male": 0})
        for col in ["pclass", "age", "fare", "sib_sp", "parch"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        corr = df[["survived", "gender", "pclass", "age", "fare", "sib_sp", "parch"]].corr()["survived"].drop("survived")
        top = corr.abs().idxmax()
        top_val = corr[top]

        direction = "여성일수록" if top == "gender" else f"{top}이 높을수록"
        return (
            f"생존에 가장 큰 영향을 미친 요인은 '{top}'입니다. "
            f"{direction} 생존율이 {'높았' if top_val > 0 else '낮았'}습니다. "
            f"그 다음으로는 객실 등급(pclass)과 요금(fare)이 중요한 역할을 했습니다."
        )

    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        '''앤드류 설계자의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(AndrewsArchitectQuery(
            id = schema.id,
            name = schema.name
        ))
