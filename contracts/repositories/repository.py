from typing import TypeVar, Protocol

T = TypeVar("T")


class Repository(Protocol[T]):
    @classmethod
    async def create(cls, **kwargs) -> None:
        ...

    @classmethod
    async def update(cls, **kwargs) -> None:
        ...

    @classmethod
    async def delete(cls, **kwargs) -> None:
        ...

    @classmethod
    async def get_all(cls) -> list[T]:
        ...

    @classmethod
    async def get_by_id(cls, id: int) -> T:
        ...
