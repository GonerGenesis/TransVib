import decimal
from typing import Optional, List, Annotated, TYPE_CHECKING

import strawberry

from .msg import MsgType
from ..db.schemas import FramePointSchemaCreate, FramePointSchema, UpdateFramePoint, FramePointSchemaCreateImport
from ..db import functions as funcs

if TYPE_CHECKING:
    from .frame_segment import FrameSegmentType
    from .frame import FrameType


# @strawberry.experimental.pydantic.type(model=FramePointSchema)
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


@strawberry.experimental.pydantic.input(model=UpdateFramePoint, all_fields=True)
class FramePointUpdate:
    pass

@strawberry.experimental.pydantic.input(model=FramePointSchemaCreateImport, all_fields=True)
class FramePointImport:
    pass


@strawberry.field
async def get_point(self, id: int) -> FramePointType:
    return await funcs.point.get(id=id)


@strawberry.mutation
async def create_point(self, point: FramePointInput) -> FramePointType:
    point_obj = await funcs.point.create(point.to_pydantic())
    return point_obj


@strawberry.mutation
async def update_point(self, point_id: int, point: FramePointUpdate) -> FramePointType:
    obj_in: UpdateFramePoint = point.to_pydantic()
    point: FramePointSchema = await funcs.point.update(id=point_id, obj_in=obj_in)
    return point


@strawberry.mutation
async def delete_point(self, id: int) -> MsgType:
    return await funcs.point.delete(id=id)
