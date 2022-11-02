from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import FramePoint


class UpdateFramePoint(BaseModel):
    y: Optional[float]
    z: Optional[float]


FramePointSchemaCreate = pydantic_model_creator(
    FramePoint, name=f"{FramePoint.__name__}SchemaCreate", exclude_readonly=True
)

FramePointSchema = pydantic_model_creator(
    FramePoint, name=f"{FramePoint.__name__}Schema", exclude=("frame",)
)
