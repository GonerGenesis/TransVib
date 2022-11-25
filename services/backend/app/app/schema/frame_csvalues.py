from typing import TYPE_CHECKING, Annotated
from datetime import datetime

import strawberry
from strawberry.types import Info
from tortoise.contrib.pydantic import PydanticModel

from ..core.config import Settings
from ..db.schemas import FrameCSValuesSchema
from ..db import functions as funcs

from ..worker import calc_frame_properties
from app.db.models import FrameCSValues

if TYPE_CHECKING:
    from .frame import FrameType


@strawberry.input
class PointInput:
    y: float
    z: float


@strawberry.type()
class PointType:
    y: float
    z: float


@strawberry.type
class FrameCSValuesType:
    frame_id: int
    frame: Annotated['FrameType', strawberry.lazy('.frame')]
    created_at: datetime
    modified_at: datetime
    # y = fields.DecimalField(max_digits=9, decimal_places=3)
    # z = fields.DecimalField(max_digits=9, decimal_places=3)
    center: 'PointType'
    area: float
    aqy: float
    aqz: float
    ay: float
    az: float
    ayy: float
    azz: float
    ayz: float
    ayys: float
    azzs: float
    ayzs: float
    phi: float
    i1: float
    i2: float
    ir1: float
    ir2: float
    # shear_y = fields.DecimalField(max_digits=9, decimal_places=3)
    # shear_z = fields.DecimalField(max_digits=9, decimal_places=3)
    shear_center: 'PointType'
    it: float
    awwm: float


@strawberry.input
class FrameCSValuesInput:
    frame_id: int
    # y = fields.DecimalField(max_digits=9, decimal_places=3)
    # z = fields.DecimalField(max_digits=9, decimal_places=3)
    center: 'PointInput'
    area: float
    aqy: float
    aqz: float
    ay: float
    az: float
    ayy: float
    azz: float
    ayz: float
    ayys: float
    azzs: float
    ayzs: float
    phi: float
    i1: float
    i2: float
    ir1: float
    ir2: float
    # shear_y = fields.DecimalField(max_digits=9, decimal_places=3)
    # shear_z = fields.DecimalField(max_digits=9, decimal_places=3)
    shear_center: 'PointInput'
    it: float
    awwm: float


@strawberry.field
async def get_cs_values(self, id: int, info: Info) -> FrameCSValuesType:
    settings: Settings = info.context['settings']
    print(settings)
    r = calc_frame_properties.apply_async(args=[id, settings.database], queue='main-queue')
    print("calc done:", r.get())
    model = await FrameCSValues.filter(frame_id=id).first()


    if not model:
        raise Exception("item not found")

    if issubclass(FrameCSValuesSchema, PydanticModel):
        result = (await FrameCSValuesSchema.from_tortoise_orm(model)).dict()
        result["center"] = PointType(**result["center"])
        result["shear_center"] = PointType(**result["shear_center"])
        print("calcs", result)
        return FrameCSValuesType(**result)
    return model
    # return await funcs.csvalues.get(frame_id=id)

# @strawberry.mutation
# async def create_cs_values(self, cs_values: FrameCSValuesInput) -> FrameCSValuesType:
#     cs_values_obj = await funcs.csvalues.create(cs_values)
#     return cs_values_obj
