from fastapi import HTTPException

from ..models import Ship
from .base import CRUDBase
from ..schemas.ships import ShipSchema, ShipSchemaCreate, UpdateShip


class CRUDShip(CRUDBase[Ship, ShipSchema, ShipSchemaCreate, UpdateShip]):
    pass
    # async def create_frame(self, frame_in: FrameSchemaCreate):
    #     frame_obj = await self.create_frame_obj(frame_in)
    #     return await FrameSchema.from_tortoise_orm(await frame_obj)
    #
    # async def create_frame_obj(self, frame_in: FrameSchemaCreate):
    #     try:
    #         frame_obj = await Frame.create(**{"frame_pos": frame_in.frame_pos, "ship_id": frame_in.ship_id})
    #     except IntegrityError:
    #         raise HTTPException(status_code=401, detail=f"Sorry, that frame exists.")
    #
    #     return frame_obj


ship = CRUDShip(Ship, ShipSchema)


# async def create_ship(self, title: str, description: str = ""):
#     print(locals())
#     dict_in = locals()
#     dict_in.pop('self')
#     dict_in['author_id'] = 1
#     obj_in: ShipSchemaCreate = ShipSchemaCreate(**dict_in)
#     return await ship.create(obj_in)
#
#
# async def get_ship(self, id: int):
#     return await ship.get(id)
