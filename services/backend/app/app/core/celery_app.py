import asyncio
import os

from celery import Celery
from celery.signals import celeryd_init, task_prerun, task_received, task_postrun
from tortoise import Tortoise
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery("worker", backend='rpc://', broker="amqp://guest@queue//")

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue", "app.worker.calc_frame_properties": "main-queue"}


async def init(test: bool = False):
    connections = {"default": os.environ.get("DATABASE_URL")}
    if test:
        connections['default'] = os.environ.get("DATABASE_TEST_URL")
    await Tortoise.init(
        config={
            "connections": connections,
            "apps": {
                "models": {
                    "models": ["app.db.models.models"],
                    "default_connection": "default",
                }
            },
        }
        # db_url=,
        # modules={"models": ["app.database.models"]},
    )
    logger.info("conns initialized")
    # logger.info(Tortoise.get_connection('default'))


# @task_prerun.connect
# def configure_workers(task_id, task, **kwargs):
#     logger.info("get DB connection")
#     logger.info(task)
#     asyncio.run(init(test=kwargs.get('test')))
#
# @task_postrun.connect
# def configure_workers(sender=None, conf=None, **kwargs):
#     logger.info("close DB connection")
#     asyncio.run(Tortoise.close_connections())
