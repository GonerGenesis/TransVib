# from raven import Client
import nest_asyncio
from tortoise import Tortoise

from app.core.celery_app import celery_app
from app.calc.csvalues import utils
# from asgiref.sync import async_to_sync
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# from app import schemas, crud, models

# client_sentry = Client(settings.SENTRY_DSN)
# nest_asyncio.apply()


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task
def calc_frame_properties(frame_id: int, conn_name: str = 'default'):
    # print(repr(frame))
    # frame = schemas.FrameWithGeometry.parse_obj(frame)
    # frame = models.Frame(**frame)
    # print("with geo", frame)
    logging.info("starting calculation")
    loop = asyncio.get_event_loop()
    r = loop.run_until_complete(utils.calc_frame_properties(frame_id, conn_name=conn_name, debug=True))
    # r = async_to_sync(utils.calc_frame_properties)(frame_id, test=test, debug=True)
    # r = utils.calc_frame_properties(frame_id, test=test, debug=True)
    return r
