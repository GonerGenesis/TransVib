# import app
# from celery import Celery
import asyncio
import logging
from typing import List

import nest_asyncio
import networkx as nx
from tortoise import Tortoise, BaseDBAsyncClient, connections
from tortoise.contrib.pydantic import PydanticListModel
from tortoise.fields import ReverseRelation
from tortoise.transactions import in_transaction

from ...db.models import Frame, FrameCSValues, FrameSegment
from ...db.schemas import FrameSchema, FrameSegmentSchema
from app.calc.csvalues import cs_inertia, cs_torsion
from app.core.config import get_settings, TORTOISE_ORM
from .frame_calculations import FrameCalculations

nest_asyncio.apply()
# from . import info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init(conn: str):
    # connections = {"default": os.environ.get("DATABASE_URL")}
    # if test:
    #    connections['default'] = os.environ.get("DATABASE_TEST_URL")
    config = TORTOISE_ORM
    config['apps']['models']['default_connection']=conn
    await Tortoise.init(
        config=config
        # db_url=,
        # modules={"models": ["app.database.models"]},
    )
    logger.info("conns initialized")
    # logger.info(Tortoise.get_connection('default'))
    return connections.get(conn)

class AlreadyUpToDateException(Exception):
    def __init__(self):
        super.__init__("frame properties are already up to date")


async def calc_frame_properties(frame_id: int, conn_name: str = 'default', debug=False):
    logger.info("calculation setup")
    # if test:
    #     conn_name = "test"
    # else:
    #     conn_name = "default"
    # # logger.info(in_transaction())
    try:
        await init(conn_name)
        # connection: BaseDBAsyncClient = connections.get(conn_name)
        # logger.info(connection.connection_name)
        # logger.info(await FrameSchema.from_queryset_single(Frame.get(id=frame_id)))
        # logger.info(await Frame.filter(id=frame_id).using_db(conn).first())
        # logger.info(await Frame.filter(id=frame_id).using_db(conn).prefetch_related('frame_points'))
        frame: Frame = await Frame.get(id=frame_id).prefetch_related('ship', 'cs_values', 'frame_segments', 'frame_points')
        # frame: Frame = await Frame.filter(id=frame_id).using_db(conn).first()
        # frame: FrameSchema = await FrameSchema.from_queryset_single(Frame.filter(id=frame_id).using_db(conn).first())
        logger.info("frame: %s", frame.__dict__)
        # await frame.fetch_related('ship', 'cs_values', 'frame_segments', 'frame_points')
        # logger.info("frame: %s", frame.__dict__)
        frame_segments = frame.frame_segments
        frame_props: FrameCSValues = frame.cs_values
        logger.info("frame_props: %s", frame_props)
        logger.info("frame_segments: %s", frame.frame_segments)
        logger.info("frame_segments_objects: %s", frame.frame_segments.related_objects)
        if frame_props:
            if frame_props.modified_at >= frame.modified_at:
                raise AlreadyUpToDateException
        await write_results_to_db(frame, frame_props)
            # print("watchme2")
        # if debug:
        #     fig = OmegaPlot(graph).fig
        #     fig.show()
    finally:
        await Tortoise.close_connections()
    return True


async def write_results_to_db(frame: Frame, frame_props: FrameCSValues):
    graph = nx.Graph()
    frame_segments = frame.frame_segments
    logger.info("frame_segments: {}".format(frame_segments))
    edge: FrameSegment
    for edge in frame_segments:
        # logger.info("edge: %s", edge.fetch_related())
        egde = edge
        logger.info("p1: %s, p2: %s", await edge.start_point.first(), await edge.end_point.first())
        graph.add_edge(await edge.start_point.first(), await edge.end_point.first(), thick=float(edge.thick))
    logger.info(graph)
    calc_frame = FrameCalculations(graph, logger)
    inertia: cs_inertia.CrossSectionInertiaValues = calc_frame.cs_inertia
    torsion: cs_torsion.CrossSectionTorsionValues = calc_frame.cs_torsion
    frame_props_in_dict = {'frame_id': frame.id, 'center': (inertia.a_vals.y_s, inertia.a_vals.z_s),
                           'area': inertia.a_vals.a, 'aqy': inertia.a_vals.aqy, 'aqz': inertia.a_vals.aqz,
                           'ay': inertia.a_vals.ay, 'ayy': inertia.a_vals.ayy, 'az': inertia.a_vals.az,
                           'azz': inertia.a_vals.azz, 'ayz': inertia.a_vals.ayz, 'azzs': inertia.a_vals.azzs,
                           'ayys': inertia.a_vals.ayys, 'ayzs': inertia.a_vals.ayzs, 'phi': inertia.main_axis_vals.phi,
                           'i1': inertia.main_axis_vals.I1, 'i2': inertia.main_axis_vals.I2,
                           'ir1': inertia.main_axis_vals.i1,
                           'ir2': inertia.main_axis_vals.i2, 'shear_center': (torsion.y_m, torsion.z_m),
                           'it': torsion.it,
                           'awwm': torsion.awwm}
    frame_props_in = FrameCSValues(**frame_props_in_dict)
    print(frame_props)
    if frame_props:
        print("update")
        await frame_props.delete()
    await frame_props_in.save()
