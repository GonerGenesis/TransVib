import decimal
from typing import Optional, List, Annotated, TYPE_CHECKING

import strawberry

from ..db.schemas import FramePointSchemaCreate, FramePointSchema
from ..db import functions as funcs

if TYPE_CHECKING:
    from .frame_segment import FrameSegmentType
    from .frame import FrameType


#@strawberry.experimental.pydantic.type(model=FramePointSchema)
@strawberry.type
class FramePointType:
    id: int
    y: decimal.Decimal
    z: decimal.Decimal
    frame: Annotated["FrameType", strawberry.lazy('.frame')]
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
