from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class HeroQueryParamsDto(BaseModel):
    name: Optional[str] = Query(None)

    intelligence: Optional[int] = Query(None)
    intelligence__gte: Optional[int] = Query(None)
    intelligence__lte: Optional[int] = Query(None)

    strength: Optional[int] = Query(None)
    strength__gte: Optional[int] = Query(None)
    strength__lte: Optional[int] = Query(None)

    speed: Optional[int] = Query(None)
    speed__gte: Optional[int] = Query(None)
    speed__lte: Optional[int] = Query(None)

    power: Optional[int] = Query(None)
    power__gte: Optional[int] = Query(None)
    power__lte: Optional[int] = Query(None)
