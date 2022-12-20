from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import Frame
from .points import FramePointSchemaCreateImport
from .segments import FrameSegmentSchemaImport


class UpdateFrame(BaseModel):
    frame_pos: Optional[float]


class FrameGeometry(BaseModel):
    frame_points: list[FramePointSchemaCreateImport]
    frame_segments: list[FrameSegmentSchemaImport]


class FrameSchemaCreateWithGeo(BaseModel):
    frame_pos: float
    ship_id: int
    frame_geometry: Optional[FrameGeometry]


FrameSchemaCreate = pydantic_model_creator(
    Frame, name=f"{Frame.__name__}SchemaCreate", exclude_readonly=True
)

FrameSchema = pydantic_model_creator(
    Frame, name=f"{Frame.__name__}Schema",
)
