import asyncio
import os

from celery import Celery
from celery.signals import celeryd_init, task_prerun, task_received, task_postrun
from tortoise import Tortoise
import logging

from app.core.config import TORTOISE_ORM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery("worker", backend='rpc://', broker="amqp://guest@queue//")

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue", "app.worker.calc_frame_properties": "main-queue"}


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
