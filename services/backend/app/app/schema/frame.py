from typing import Optional, List, Annotated, TYPE_CHECKING

import strawberry

from .msg import MsgType
from ..db.schemas import FrameSchemaCreate, FrameSchema, UpdateFrame
from ..db import functions as funcs

if TYPE_CHECKING:
    from .frame_csvalues import FrameCSValuesType
    from .frame_point import FramePointType
    from .frame_segment import FrameSegmentType
    from .ship import ShipType


#@strawberry.experimental.pydantic.type(model=FrameSchema)
@strawberry.type
class FrameType:
    id: int
    frame_pos: float
    cs_values: Annotated["FrameCSValuesType", strawberry.lazy(".frame_csvalues")]
    frame_segments: List[Annotated["FrameSegmentType", strawberry.lazy(".frame_segment")]]
    frame_points: List[Annotated["FramePointType", strawberry.lazy(".frame_point")]]
    ship: Annotated["ShipType", strawberry.lazy('.ship')]


@strawberry.experimental.pydantic.input(model=FrameSchemaCreate, all_fields=True)
class FrameInput:
    pass

@strawberry.experimental.pydantic.input(model=UpdateFrame, all_fields=True)
class FrameUpdate:
    pass

@strawberry.field
async def get_frame(self, id: int) -> FrameType:
    return await funcs.frame.get(id=id)

@strawberry.mutation
async def create_frame(self, frame: FrameInput) -> FrameType:
    frame_obj = await funcs.frame.create(frame.to_pydantic())
    return frame_obj

@strawberry.mutation
async def update_frame(self, frame_id: int, frame: FrameUpdate) -> FrameType:
    obj_in: UpdateFrame = frame.to_pydantic()
    frame: FrameSchema = await funcs.frame.update(id=frame_id, obj_in=obj_in)
    return frame


@strawberry.mutation
async def delete_frame(self, id: int) -> MsgType:
    return await funcs.frame.delete(id=id)
