from __future__ import annotations
from typing import Any

import pandas as pd
from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_port import CalTesterPort

import logging

logger = logging.getLogger(__name__)

class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTesterPort):
        self.repository = repository
        self.kiwi = Kiwi()

    async def test_model(self, test_set: dict[str, Any]) -> dict[str, Any]:
        '''칼이 로즈가 제안한 10개 모델의 트레이닝 정도를 점수화 해서 1등을 뽑는것

        Args:
            test_set: {
                "df":                pd.DataFrame,
                "trained_strategies": dict[str, strategy],
            }
        '''
        logger.info("[CalTesterInteractor] 모델 채점 시작")

        trained_strategies: dict[str, Any] = test_set["trained_strategies"]
        X_test, y_test = _preprocess_test(test_set["df"])

        results: list[dict[str, Any]] = []
        for key, strategy in trained_strategies.items():
            try:
                predictions = strategy.predict(X_test)
                correct = sum(p == t for p, t in zip(predictions, y_test))
                accuracy = correct / len(y_test)
                results.append({
                    "key": key,
                    "name": key,
                    "accuracy": round(accuracy, 4),
                    "correct": correct,
                    "total": len(y_test),
                })
                logger.info(f"[CalTesterInteractor] {key} | accuracy={accuracy:.4f}")
            except Exception as e:
                results.append({
                    "key": key,
                    "name": key,
                    "accuracy": None,
                    "error": str(e),
                })
                logger.warning(f"[CalTesterInteractor] {key} 채점 실패 | error={e}")

        results.sort(key=lambda r: r.get("accuracy") or -1, reverse=True)
        for i, r in enumerate(results):
            r["rank"] = i + 1

        champion = results[0] if results else None
        logger.info(f"[CalTesterInteractor] 챔피언 결정 | {champion}")

        return {
            "test_samples": len(X_test),
            "champion": champion,
            "ranking": results,
        }

    async def analyze_message_intent(self, user_message: str) -> dict:
        '''사용자의 질문(message)을 형태소 분석하여 키워드와 의도를 파악한다'''
        logger.info(f"[CalTesterInteractor] 분석 시작 | message: {user_message}")

        tokens = self.kiwi.tokenize(user_message)
        keywords = []
        has_quantity_modifier = False
        has_count_unit = False

        for t in tokens:
            if t.tag in ("NNG", "NNP"):
                keywords.append(t.form)
            if t.tag == "MM" and t.form == "몇":
                has_quantity_modifier = True
            if t.tag == "NNB" and t.form in ("명", "개", "사람", "분"):
                has_count_unit = True

        is_count_query = has_quantity_modifier or has_count_unit or ("몇" in user_message)
        result = {"keywords": keywords, "is_count_query": is_count_query}
        logger.info(f"[CalTesterInteractor] 분석 완료 | 결과: {result}")
        return result

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        return await self.repository.introduce_myself(CalTesterQuery(
            id=schema.id,
            name=schema.name,
        ))


def _preprocess_test(df: pd.DataFrame) -> tuple[list[list[float]], list[int]]:
    """테스트 데이터 전처리 → (X_test, y_test)"""
    test = df.copy()

    test["survived"] = pd.to_numeric(test["survived"], errors="coerce")
    test = test.dropna(subset=["survived"])
    y_test = test["survived"].astype(int).tolist()
    test = test.drop("survived", axis=1)

    test["gender"] = test["gender"].map({"male": 0, "female": 1})
    test["age"] = pd.to_numeric(test["age"], errors="coerce").fillna(29.7)
    test["embarked"] = test["embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3}).fillna(1)
    test["fare"] = pd.to_numeric(test["fare"], errors="coerce").fillna(32.2)
    test["pclass"] = pd.to_numeric(test["pclass"], errors="coerce").fillna(3)
    test["sib_sp"] = pd.to_numeric(test["sib_sp"], errors="coerce").fillna(0)
    test["parch"] = pd.to_numeric(test["parch"], errors="coerce").fillna(0)

    feature_cols = ["gender", "age", "sib_sp", "parch", "pclass", "fare", "embarked"]
    test = test[feature_cols]

    return test.values.tolist(), y_test
