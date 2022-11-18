from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import Frame
from .points import UpdateFramePoint
from .segments import UpdateFrameSegment


class UpdateFrame(BaseModel):
    frame_pos: Optional[float]


class FrameSchemaCreateWithGeo(BaseModel):
    frame_pos: float
    ship_id: int
    frame_points: Optional[list[UpdateFramePoint]]
    frame_segments: Optional[list[UpdateFrameSegment]]


FrameSchemaCreate = pydantic_model_creator(
    Frame, name=f"{Frame.__name__}SchemaCreate", exclude_readonly=True
)

FrameSchema = pydantic_model_creator(
    Frame, name=f"{Frame.__name__}Schema",
)
