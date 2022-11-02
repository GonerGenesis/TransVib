from fastapi import HTTPException

from ..models import FrameSegment
from .base import CRUDBase
from ..schemas.segments import FrameSegmentSchema, FrameSegmentSchemaCreate, UpdateFrameSegment


class CRUDSegment(CRUDBase[FrameSegment, FrameSegmentSchema, FrameSegmentSchemaCreate, UpdateFrameSegment]):
    pass
    # async def create_frame(self, frame_in: FrameSchemaCreate):
    #     frame_obj = await self.create_frame_obj(frame_in)
    #     return await FrameSchema.from_tortoise_orm(await frame_obj)
    #
    # async def create_frame_obj(self, frame_in: FrameSchemaCreate):
    #     try:
    #         frame_obj = await Frame.create(**{"frame_pos": frame_in.frame_pos, "ship_id": frame_in.ship_id})
    #     except IntegrityError:
    #         raise HTTPException(status_code=401, detail=f"Sorry, that frame exists.")
    #
    #     return frame_obj


segment = CRUDSegment(FrameSegment, FrameSegmentSchema)


async def create_segment(self, frame_id: int, start_point_id: int, end_point_id: int, thick: float):
    print(locals())
    dict_in = locals()
    dict_in.pop('self')
    obj_in: FrameSegmentSchemaCreate = FrameSegmentSchemaCreate(**dict_in)
    return await segment.create(obj_in)


async def get_segment(self, id: int):
    return await segment.get(id)
