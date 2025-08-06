from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse

from config import get_config
from contracts.dto.hero_dto import HeroDTO
from contracts.dto.hero_query_params_dto import HeroQueryParamsDto
from database.models.hero import Hero
from database.repositories.hero_repository import HeroRepository
from error_statuses import error_statuses
from handlers.hero_handler import HeroHandler

router = APIRouter()


async def get_hero_handler():
    return HeroHandler(
        hero_repository=HeroRepository(Hero()),
        config=get_config()
    )


@router.post("/hero/")
async def search_and_create_hero(hero_dto: HeroDTO, handler: Annotated[HeroHandler, Depends(get_hero_handler)]):
    created_heroes_list = await handler.search_and_create_hero(hero_dto.name.strip())

    if isinstance(created_heroes_list, str):
        raise HTTPException(status_code=error_statuses[created_heroes_list], detail=created_heroes_list.capitalize())

    return JSONResponse(status_code=201, content={"status": "success", "results": created_heroes_list})


@router.get("/hero/", response_model=list[HeroDTO])
async def get_heroes(
        handler: Annotated[HeroHandler,
        Depends(get_hero_handler)], query_params: HeroQueryParamsDto = Depends()
):
    filters = {}

    for key, value in query_params.model_dump().items():
        if value:
            filters[key] = value.strip().lower().capitalize() if key == "name" else value

    if not filters:
        return JSONResponse(
            status_code=200,
            content=[hero.model_dump() for hero in await handler.get_all()]
        )

    heroes = await handler.get_by_filter(**filters)

    if not heroes:
        return JSONResponse(status_code=404, content={"message": "No heroes found."})

    return JSONResponse(status_code=200, content=[hero.model_dump() for hero in heroes])
