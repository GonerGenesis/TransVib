# project/app/db.py


import logging
import sys

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import TORTOISE_ORM

#from app.core.config import get_settings

log = logging.getLogger("uvicorn")

# settings = get_settings()


async def init_db(app: FastAPI) -> None:
    fmt = logging.Formatter(
        fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(fmt)
    logger_tortoise = logging.getLogger("tortoise")
    logger_tortoise.setLevel(logging.DEBUG)
    logger_tortoise.addHandler(sh)
    register_tortoise(
        app,
        # db_url=settings.database_url,
        # modules={"models": ["app.db.models.models"]},
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )
    # from app.schemas import Ship
    # ship = await Ship.all()



async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    # await Tortoise.init(
    #     db_url=settings.database_url,
    #     modules={"models": ["app.db.models.models"]},
    # )
    await Tortoise.init(
        config=TORTOISE_ORM
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
