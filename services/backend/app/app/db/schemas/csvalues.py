from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import FrameCSValues






# class UpdateFrameSegment(BaseModel):
#     start_point_id: Optional[int]
#     end_point_id: Optional[int]
#     thick: Optional[float]

# class FrameCSValuesSchemaCreate(BaseModel):
#     # update_time: datetime = Field(default_factory=datetime.utcnow)
#     frame_id: int
#     center: tuple
#     area: float
#     aqy: float
#     aqz: float
#     ay: float
#     az: float
#     ayy: float
#     azz: float
#     ayz: float
#     ayys: float
#     azzs: float
#     ayzs: float
#     phi: float
#     i1: float
#     i2: float
#     ir1: float
#     ir2: float
#     shear_center: tuple
#     it: float
#     awwm: float
#
#
class PydanticPoint(BaseModel):
    y: float
    z: float

    def dict(self, *args, **kwargs):
        return {"y": self.y ,"z":self.z}


class FrameCSValuesSchemaUpdate(BaseModel):
    center: Optional[PydanticPoint]
    area: Optional[float]
    aqy: Optional[float]
    aqz: Optional[float]
    ay: Optional[float]
    az: Optional[float]
    ayy: Optional[float]
    azz: Optional[float]
    ayz: Optional[float]
    ayys: Optional[float]
    azzs: Optional[float]
    ayzs: Optional[float]
    phi: Optional[float]
    i1: Optional[float]
    i2: Optional[float]
    ir1: Optional[float]
    ir2: Optional[float]
    shear_center: Optional[PydanticPoint]
    it: Optional[float]
    awwm: Optional[float]
#
#
# class FrameCSValuesSchema(FrameCSValuesSchemaCreate):
#     id: Optional[int]
#     modified_at: Optional[datetime]
FrameCSValuesSchemaCreate = pydantic_model_creator(
    FrameCSValues, name=f"{FrameCSValues.__name__}SchemaCreate", exclude=("frame", "created_at", "modified_at"),
)

# FrameCSValuesSchemaUpdate = pydantic_model_creator(
#     FrameCSValues, name=f"{FrameCSValues.__name__}SchemaUpdate", exclude_readonly=True,
# )

FrameCSValuesSchema = pydantic_model_creator(
    FrameCSValues, name=f"{FrameCSValues.__name__}Schema", exclude=("frame",)
)
