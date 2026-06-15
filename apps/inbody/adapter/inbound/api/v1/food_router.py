from __future__ import annotations

from fastapi import APIRouter, Depends

from inbody.adapter.inbound.api.schemas.food_schema import FoodCreateRequest, FoodResponse
from inbody.app.dtos.food_dto import FoodCreateCommand, FoodDto, FoodSearchQuery
from inbody.app.ports.input.food_use_case import FoodUseCase
from inbody.dependencies.food_provider import get_food_use_case

router = APIRouter(prefix="/inbody", tags=["inbody-food"])


def _dto_to_resp(dto: FoodDto) -> FoodResponse:
    return FoodResponse(
        id=dto.id,
        name=dto.name,
        caloriesKcal=dto.calories_kcal,
        proteinG=dto.protein_g,
        carbsG=dto.carbs_g,
        fatG=dto.fat_g,
        servingSize=dto.serving_size,
        servingUnit=dto.serving_unit,
        createdBy=dto.created_by,
    )


@router.get("/foods", response_model=list[FoodResponse])
async def search_foods(
    query: str,
    use_case: FoodUseCase = Depends(get_food_use_case),
):
    dtos = await use_case.search(FoodSearchQuery(keyword=query))
    return [_dto_to_resp(d) for d in dtos]


@router.post("/foods", response_model=FoodResponse, status_code=201)
async def create_food(
    req: FoodCreateRequest,
    use_case: FoodUseCase = Depends(get_food_use_case),
):
    command = FoodCreateCommand(
        name=req.name,
        calories_kcal=req.caloriesKcal,
        protein_g=req.proteinG,
        carbs_g=req.carbsG,
        fat_g=req.fatG,
        serving_size=req.servingSize,
        serving_unit=req.servingUnit,
        created_by=req.userId,
    )
    dto = await use_case.create(command)
    return _dto_to_resp(dto)
