from contracts.repositories.repository import Repository
from database.models.hero import Hero


class HeroRepository(Repository[Hero]):
    def __init__(self, model: Hero):
        self._model: Hero = model

    async def create(self, **kwargs) -> None:
        await self._model.create(**kwargs)

    async def update(self, **kwargs) -> None:
        await self._model.update_from_dict(kwargs)

    async def delete(self, id: int) -> None:
        hero = await self._model.get(id=id)
        hero.is_deleted = True
        await hero.save()

    async def get_all(self) -> list[Hero]:
        return await self._model.all()

    async def get_by_id(self, id: int) -> Hero:
        return await self._model.get(id=id)

    async def get_by_filters(self, **kwargs) -> list[Hero]:
        return await self._model.filter(**kwargs).all()