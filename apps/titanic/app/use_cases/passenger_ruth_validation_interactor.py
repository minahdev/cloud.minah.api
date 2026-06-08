from __future__ import annotations

import logging
from typing import Any

from minahai.apps.titanic.app.ports.input.passenger_ruth_validation_use_case import RuthCorsetUseCase

logger = logging.getLogger()


def _validate_passenger(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not str(data.get("passengerId", "")).strip():
        errors.append("passengerId is required")
    age = str(data.get("age", "")).strip()
    if age:
        try:
            age_val = float(age)
            if age_val < 0 or age_val > 120:
                errors.append("age must be between 0 and 120")
        except ValueError:
            errors.append("age must be numeric")
    pclass = str(data.get("pclass", "")).strip()
    if pclass and pclass not in {"1", "2", "3"}:
        errors.append("pclass must be 1, 2, or 3")
    return errors


class RuthCorsetInteractor(RuthCorsetUseCase):
    async def validate_corset(self, request: dict[str, Any]) -> dict[str, Any]:
        msg = f"👗 [ruth_interactor] validate_corset | passengerId={request.get('passengerId')!r}"
        logger.info(msg)
        errors = _validate_passenger(request)
        if errors:
            return {"valid": False, "message": "Validation failed", "errors": errors}
        return {"valid": True, "message": "Validation passed", "errors": []}
