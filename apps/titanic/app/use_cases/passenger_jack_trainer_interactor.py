from __future__ import annotations

import logging
from typing import Any

from titanic.app.ports.input.passenger_jack_trainer_use_case import JackSketchUseCase

logger = logging.getLogger()


class JackSketchInteractor(JackSketchUseCase):
    async def get_sketch(self, request: dict[str, Any]) -> dict[str, Any]:
        msg = "🎨 [jack_interactor] get_sketch"
        logger.info(msg)
        subject = str(request.get("name") or request.get("passengerId") or "passenger")
        return {
            "artist": "Jack Dawson",
            "subject": subject,
            "medium": "charcoal",
            "message": "Sketch ready",
        }
