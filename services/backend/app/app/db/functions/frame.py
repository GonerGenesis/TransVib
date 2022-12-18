import logging

from fastapi import HTTPException

from ..models import Frame
from .base import CRUDBase
from ..schemas import FrameSchema, FrameSchemaCreate, UpdateFrame, FrameSchemaCreateWithGeo
import yaml

LOGGER = logging.getLogger(__name__)


class CRUDFrame(CRUDBase[Frame, FrameSchema, FrameSchemaCreate, UpdateFrame]):
    # pass
    async def create(self, frame_in: FrameSchemaCreateWithGeo):
        frame_in = frame_in.dict()
        # LOGGER.info(frame_in)
        geometry = frame_in.pop("frame_geometry")
        if geometry:
            pass
        # if "points" in frame_in:
        #     frame_in.pop("points")
        # if "segments" in frame_in:
        #     frame_in.pop("segments")
        # frame = await super().create(FrameSchemaCreate(ship_id=frame_in["ship_id"], frame_pos=frame_in["frame_pos"]))
        frame = await super().create(FrameSchemaCreate(**frame_in))
        # frame_obj = await self.create_frame_obj(frame_in)
        # return await FrameSchema.from_tortoise_orm(await frame_obj)
        return frame
    #
    # async def create_frame_obj(self, frame_in: FrameSchemaCreate):
    #     try:
    #         frame_obj = await Frame.create(**{"frame_pos": frame_in.frame_pos, "ship_id": frame_in.ship_id})
    #     except IntegrityError:
    #         raise HTTPException(status_code=401, detail=f"Sorry, that frame exists.")
    #
    #     return frame_obj


frame = CRUDFrame(Frame, FrameSchema)

# async def create_frame(self, ship_id: int, frame_pos: float):
#     print(locals())
#     dict_in = locals()
#     dict_in.pop('self')
#     obj_in: FrameSchemaCreate = FrameSchemaCreate(**dict_in)
#     return await frame.create(obj_in)
#
#
# async def get_frame(self, id: int):
#     return await frame.get(id)
