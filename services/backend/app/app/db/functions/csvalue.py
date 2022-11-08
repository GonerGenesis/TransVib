from fastapi import HTTPException

from ..models import FrameCSValues
from .base import CRUDBase
from ..schemas.csvalues import FrameCSValuesSchema, FrameCSValuesSchemaCreate, FrameCSValuesSchemaUpdate


class CRUDFrameCSValues(CRUDBase[FrameCSValues, FrameCSValuesSchema, FrameCSValuesSchemaCreate, FrameCSValuesSchemaUpdate]):
    pass
    # async def create_csvalues(self, csvalues_in: FrameCSValuesSchemaCreate):
    #     csvalues_obj = await self.create_csvalues_obj(csvalues_in)
    #     return await FrameCSValuesSchema.from_tortoise_orm(await csvalues_obj)
    #
    # async def create_csvalues_obj(self, csvalues_in: FrameCSValuesSchemaCreate):
    #     try:
    #         csvalues_obj = await FrameCSValues.create(**{"csvalues_pos": csvalues_in.csvalues_pos, "ship_id": csvalues_in.ship_id})
    #     except IntegrityError:
    #         raise HTTPException(status_code=401, detail=f"Sorry, that csvalues exists.")
    #
    #     return csvalues_obj


csvalues = CRUDFrameCSValues(FrameCSValues, FrameCSValuesSchema)


async def create_csvalues(self, center: tuple[float, float], area: float, aqy: float, aqz: float, ay: float, az: float, ayy: float, azz: float, ayz: float, ayys: float, azzs: float, ayzs: float, phi: float, i1: float, i2: float, ir1: float, ir2: float, shear_center: tuple[float, float], it: float, awwm: float):
    print(locals())
    dict_in = locals()
    dict_in.pop('self')
    obj_in: FrameCSValuesSchemaCreate = FrameCSValuesSchemaCreate(**dict_in)
    return await csvalues.create(obj_in)


async def get_csvalues(self, id: int):
    return await csvalues.get(id)
