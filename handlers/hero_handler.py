from tortoise.exceptions import IntegrityError

from config import Config
from contracts.dto.hero_dto import HeroDTO
from database.models.hero import Hero
from database.repositories.hero_repository import HeroRepository
from utils.http_client import HttpClient


class HeroHandler:
    def __init__(self, hero_repository: HeroRepository, config: Config):
        self._repository: HeroRepository = hero_repository
        self._config: Config = config

    async def search_and_create_hero(self, hero_name: str) -> list[HeroDTO] | str:
        hero_info = await HttpClient.search_hero(hero_name)

        if hero_info["response"] == "error":
            return hero_info["error"]

        dto_list = []

        for hero in hero_info.get("results", []):
            if hero_name.lower() == hero["name"].lower():
                stats = hero["powerstats"]

                dto = HeroDTO(
                    id=hero["id"],
                    name=hero["name"],
                    intelligence=stats["intelligence"] if stats["intelligence"] != "null" else None,
                    strength=stats["strength"] if stats["strength"] != "null" else None,
                    speed=stats["speed"] if stats["speed"] != "null" else None,
                    power=stats["power"] if stats["power"] != "null" else None
                )

                try:
                    dto_dict = dto.model_dump()
                    await self._repository.create(**dto_dict)
                    dto_list.append(dto_dict)
                except IntegrityError:
                    continue

        if not dto_list:
            return "Heroes already exist in the database."

        return dto_list

    async def get_all(self):
        return [HeroDTO(
            id=hero.id,
            name=hero.name,
            intelligence=hero.intelligence,
            strength=hero.strength,
            speed=hero.speed,
            power=hero.power
        ) for hero in await self._repository.get_all()]

    async def get_by_filter(self, **kwargs) -> list[HeroDTO] | None:
        filters = {}

        for key, value in kwargs.items():
            if value:
                filters[key] = value

        return [HeroDTO(
            id=hero.id,
            name=hero.name,
            intelligence=hero.intelligence,
            strength=hero.strength,
            speed=hero.speed,
            power=hero.power
        ) for hero in await self._repository.get_by_filters(**filters)]
