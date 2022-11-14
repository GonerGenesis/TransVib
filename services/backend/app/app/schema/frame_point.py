from typing import Optional, List, Annotated, TYPE_CHECKING

import strawberry

from ..db.schemas import FramePointSchemaCreate
from ..db import functions as funcs

if TYPE_CHECKING:
    from .frame_segment import FrameSegmentType


@strawberry.type
class FramePointType:
    id: int
    y: float
    z: float
    starts_segments: List[Annotated["FrameSegmentType", strawberry.lazy('.frame_segment')]]
    ends_segments: List[Annotated["FrameSegmentType", strawberry.lazy('.frame_segment')]]


@strawberry.experimental.pydantic.input(model=FramePointSchemaCreate, all_fields=True)
class FramePointInput:
    pass


@strawberry.field
async def get_point(self, id: int) -> FramePointType:
    return await funcs.point.get(id=id)


@strawberry.mutation
async def create_point(self, point: FramePointInput) -> FramePointType:
    point_obj = await funcs.point.create(point.to_pydantic())
    return point_obj
