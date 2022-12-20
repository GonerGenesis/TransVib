from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import FrameSegment


class UpdateFrameSegment(BaseModel):
    start_point_id: Optional[int]
    end_point_id: Optional[int]
    thick: Optional[float]


FrameSegmentSchemaCreate = pydantic_model_creator(
    FrameSegment, name=f"{FrameSegment.__name__}SchemaCreate", exclude_readonly=True
)


class FrameSegmentSchemaImport(BaseModel):
    start_point_id: int
    end_point_id: int
    thick: float


FrameSegmentSchema = pydantic_model_creator(
    FrameSegment, name=f"{FrameSegment.__name__}Schema",
)
