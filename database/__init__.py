from tortoise import Tortoise

from database.tortoise_config import TORTOISE_CONFIG


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_CONFIG)
    await Tortoise.generate_schemas()
