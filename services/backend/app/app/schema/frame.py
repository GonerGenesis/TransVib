from typing import Optional, List, Annotated, TYPE_CHECKING

import strawberry

from ..db.schemas import FrameSchemaCreate
from ..db import functions as funcs

if TYPE_CHECKING:
    from .frame_csvalues import FrameCSValuesType
    from .frame_point import FramePointType
    from .frame_segment import FrameSegmentType


@strawberry.type
class FrameType:
    id: int
    frame_pos: float
    cs_values: Annotated["FrameCSValuesType", strawberry.lazy(".frame_csvalues")]
    frame_segments: List[Annotated["FrameSegmentType", strawberry.lazy(".frame_segment")]]
    frame_points: List[Annotated["FramePointType", strawberry.lazy(".frame_point")]]


@strawberry.experimental.pydantic.input(model=FrameSchemaCreate, all_fields=True)
class FrameInput:
    pass

@strawberry.field
async def get_frame(self, id: int) -> FrameType:
    return await funcs.point.get(id=id)

@strawberry.mutation
async def create_frame(self, frame: FrameInput) -> FrameType:
    frame_obj = await funcs.frame.create(frame.to_pydantic())
    return frame_obj
