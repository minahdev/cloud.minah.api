from __future__ import annotations

import logging
from typing import Any

from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorBedUseCase

logger = logging.getLogger()


class IsidorBedInteractor(IsidorBedUseCase):
    async def get_bed_status(self, request: dict[str, Any]) -> dict[str, Any]:
        msg = "🛏️ [isidor_interactor] get_bed_status"
        logger.info(msg)
        pclass = str(request.get("pclass", "")).strip()
        priority = "women and children first"
        if pclass == "1":
            note = "first-class cabin assignment"
        elif pclass in {"2", "3"}:
            note = "standard berth"
        else:
            note = "berth status unknown"
        return {
            "priority": priority,
            "note": note,
            "message": "Lifeboat priority guidance",
        }
