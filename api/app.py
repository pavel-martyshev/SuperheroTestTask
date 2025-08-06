from contextlib import asynccontextmanager

from fastapi import FastAPI

import api.controllers.hero_controller as hero_controller
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Started")

    yield

    print("Stopped")


app = FastAPI(lifespan=lifespan)
app.include_router(hero_controller.router)
