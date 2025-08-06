from pydantic import BaseModel


class HeroDTO(BaseModel):
    id: int | None = None
    name: str
    intelligence: int | None = None
    strength: int | None = None
    speed: int | None = None
    power: int | None = None
