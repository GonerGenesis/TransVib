from typing import Optional, List, TYPE_CHECKING, Annotated

import strawberry

from ..db.schemas import ShipSchemaCreate, ShipSchema
from ..db import functions as funcs

if TYPE_CHECKING:
    from app.schema.frame import FrameType
    from app.schema.user import UserType


@strawberry.type
#@strawberry.experimental.pydantic.type(model=ShipSchema)
class ShipType:
    id: int
    title: str
    description: Optional[str]
    author: Annotated['UserType', strawberry.lazy('.user')]
    frames: List[Annotated["FrameType", strawberry.lazy('.frame')]]


@strawberry.experimental.pydantic.input(model=ShipSchemaCreate, all_fields=True)
class ShipInput:
    pass


@strawberry.field
async def get_ship(self, id: int) -> ShipType:
    return await funcs.ship.get(id=id)


@strawberry.mutation
async def create_ship(self, ship: ShipInput) -> ShipType:
    ship_obj: ShipSchema = await funcs.ship.create(ship.to_pydantic())
    return ship_obj
