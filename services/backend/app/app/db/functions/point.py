from fastapi import HTTPException

from ..models import FramePoint
from .base import CRUDBase
from ..schemas.points import FramePointSchema, FramePointSchemaCreate, UpdateFramePoint


class CRUDPoint(CRUDBase[FramePoint, FramePointSchema, FramePointSchemaCreate, UpdateFramePoint]):
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


point = CRUDPoint(FramePoint, FramePointSchema)


# async def create_point(self, frame_id: int, y: float, z: float):
#     print(locals())
#     dict_in = locals()
#     dict_in.pop('self')
#     obj_in: FramePointSchemaCreate = FramePointSchemaCreate(**dict_in)
#     return await point.create(obj_in)
#
#
# async def get_point(self, id: int):
#     return await point.get(id)
