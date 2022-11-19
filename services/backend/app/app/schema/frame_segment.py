from typing import Annotated, TYPE_CHECKING
import strawberry

from .msg import MsgType
from ..db.schemas import FrameSegmentSchemaCreate, FrameSegmentSchema, UpdateFrameSegment
from ..db import functions as funcs

if TYPE_CHECKING:
    from .frame_point import FramePointType
    from .frame import FrameType


#@strawberry.experimental.pydantic.type(model=FrameSegmentSchema)
@strawberry.type
class FrameSegmentType:
    id: int
    start_point: Annotated['FramePointType', strawberry.lazy('.frame_point')]
    end_point: Annotated['FramePointType', strawberry.lazy('.frame_point')]
    thick: float
    frame: Annotated['FrameType', strawberry.lazy('.frame')]


@strawberry.experimental.pydantic.input(model=FrameSegmentSchemaCreate, all_fields=True)
class FrameSegmentInput:
    pass

@strawberry.experimental.pydantic.input(model=UpdateFrameSegment, all_fields=True)
class FrameSegmentUpdate:
    pass


@strawberry.field
async def get_segment(self, id: int) -> FrameSegmentType:
    return await funcs.segment.get(id=id)


@strawberry.mutation
async def create_segment(self, segment: FrameSegmentInput) -> FrameSegmentType:
    segment_obj = await funcs.segment.create(segment.to_pydantic())
    return segment_obj

@strawberry.mutation
async def update_segment(self, segment_id: int, segment: FrameSegmentUpdate) -> FrameSegmentType:
    obj_in: UpdateFrameSegment = segment.to_pydantic()
    segment: FrameSegmentSchema = await funcs.segment.update(id=segment_id, obj_in=obj_in)
    return segment


@strawberry.mutation
async def delete_segment(self, id: int) -> MsgType:
    return await funcs.segment.delete(id=id)
