from __future__ import annotations

import logging
from typing import Any

from titanic.app.ports.input.passenger_rose_model_use_case import RoseDiamondUseCase
from titanic.app.use_cases.rose_query import RoseModel

logger = logging.getLogger()


class RoseDiamondInteractor(RoseDiamondUseCase):
    async def get_diamond(self, request: dict[str, Any]) -> dict[str, Any]:
        msg = "💎 [rose_interactor] get_diamond -> model"
        logger.info(msg)
        model = RoseModel()
        return {
            "model": model.model_name(),
            "message": "Rose survival model is ready",
            "request": request,
        }
