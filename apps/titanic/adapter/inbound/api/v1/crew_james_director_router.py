from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, File, UploadFile

from titanic.adapter.inbound.api.james_csv_parser import parse_titanic_csv_text as _parse_csv
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_crew_james_director_use_case
from titanic.app.dtos.crew_james_director_dto import JamesDirectorResponse

logger = logging.getLogger(__name__)

crew_james_director_router = APIRouter(prefix="/titanic/james", tags=["james"])


@crew_james_director_router.post("/upload", response_model=JamesDirectorResponse)
async def upload_titanic_file(
    file: UploadFile = File(...),
    james: JamesDirectorUseCase = Depends(get_crew_james_director_use_case),
)-> JamesDirectorResponse:
    return await james.upload_titanic_file(
        _parse_csv((await file.read()).decode("utf-8-sig", errors="replace"))
    )