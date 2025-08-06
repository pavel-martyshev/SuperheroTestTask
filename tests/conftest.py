import sys
from pathlib import Path
from typing import AsyncGenerator, Any

import pytest_asyncio
from tortoise import Tortoise


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db() -> AsyncGenerator[Any, None]:
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={
            "models": [
                "database.models.hero"
            ]
        },
    )
    await Tortoise.generate_schemas()

    yield

    await Tortoise._drop_databases()
