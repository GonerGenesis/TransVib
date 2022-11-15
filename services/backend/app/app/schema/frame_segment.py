from typing import Annotated, TYPE_CHECKING
import strawberry

from ..db.schemas import FrameSegmentSchemaCreate, FrameSegmentSchema
from ..db import functions as funcs

if TYPE_CHECKING:
    from .frame_point import FramePointType


@strawberry.experimental.pydantic.type(model=FrameSegmentSchema)
class FrameSegmentType:
    id: int
    start_point: Annotated['FramePointType', strawberry.lazy('.frame_point')]
    end_point: Annotated['FramePointType', strawberry.lazy('.frame_point')]
    thick: float


@strawberry.experimental.pydantic.input(model=FrameSegmentSchemaCreate, all_fields=True)
class FrameSegmentInput:
    pass


@strawberry.field
async def get_segment(self, id: int) -> FrameSegmentType:
    return await funcs.segment.get(id=id)


@strawberry.mutation
async def create_segment(self, segment: FrameSegmentInput) -> FrameSegmentType:
    segment_obj = await funcs.segment.create(segment.to_pydantic())
    return segment_obj
