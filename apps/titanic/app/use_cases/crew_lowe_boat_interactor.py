from __future__ import annotations

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import (
    LoweBoatSchema,
)
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_port import LoweBoatPort

import logging

logger = logging.getLogger(__name__)

class LoweBoatInteractor(LoweBoatUseCase):

    def __init__(self, repository: LoweBoatPort) -> None:
        self._repository = repository

    def feature_engineering(self, train_set: pd.DataFrame) -> tuple[list[list[float]], list[int]]:
        train = train_set.copy()

        # 1. Label 분리 (빈 문자열·NaN 제거)
        train["survived"] = pd.to_numeric(train["survived"], errors="coerce")
        train = train.dropna(subset=["survived"])
        y_label = train["survived"].astype(int).tolist()
        train = train.drop("survived", axis=1)

        # 2. 성별 Nominal 변환 (female=1, male=0)
        train["gender"] = train["gender"].map({"male": 0, "female": 1})

        # 3. 나이 결측치 처리
        train["age"] = pd.to_numeric(train["age"], errors="coerce").fillna(29.7)

        # 4. 승선항 Nominal 변환
        train["embarked"] = train["embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3}).fillna(1)

        # 5. 요금 처리
        train["fare"] = pd.to_numeric(train["fare"], errors="coerce").fillna(32.2)

        # 6. pclass 처리
        train["pclass"] = pd.to_numeric(train["pclass"], errors="coerce").fillna(3)

        # 7. sib_sp, parch 처리
        train["sib_sp"] = pd.to_numeric(train["sib_sp"], errors="coerce").fillna(0)
        train["parch"] = pd.to_numeric(train["parch"], errors="coerce").fillna(0)

        # 8. ML에 불필요한 문자열 컬럼 제거 + 순서 고정
        feature_cols = ["gender", "age", "sib_sp", "parch", "pclass", "fare", "embarked"]
        train = train[feature_cols]

        X_train: list[list[float]] = train.values.tolist()
        return X_train, y_label


    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:

        return await self._repository.introduce_myself(LoweBoatQuery(
            id= schema.id,
            name= schema.name
        ))