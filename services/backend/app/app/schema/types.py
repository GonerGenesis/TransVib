from datetime import datetime
from typing import Optional, List

import strawberry
from fastapi import HTTPException
from strawberry.fastapi import GraphQLRouter
from tortoise.exceptions import IntegrityError

from app.core.security import get_password_hash
from app.db.schemas import ShipSchema, ShipSchemaCreate, UserSchema, UserSchemaCreate, NoteSchema, NoteSchemaCreate, \
    FrameSchema, FrameCSValuesSchema, FramePointSchema, FrameSegmentSchema
from app.db.models import User, Ship
from app.db.functions.ship import get_ship, create_ship
from app.db.functions.user import get_user_by_id, create_user


@strawberry.experimental.pydantic.type(model=NoteSchema)
class NoteType:
    id: strawberry.auto
    title: strawberry.auto
    content: strawberry.auto
    created_at: strawberry.auto
    modified_at: strawberry.auto


@strawberry.experimental.pydantic.type(model=FrameCSValuesSchema)
class FrameCSValuesType:
    frame: 'FrameType'
    created_at: strawberry.auto
    modified_at: strawberry.auto
    # y = fields.DecimalField(max_digits=9, decimal_places=3)
    # z = fields.DecimalField(max_digits=9, decimal_places=3)
    center: tuple[float, float]
    area: strawberry.auto
    aqy: strawberry.auto
    aqz: strawberry.auto
    ay: strawberry.auto
    az: strawberry.auto
    ayy: strawberry.auto
    azz: strawberry.auto
    ayz: strawberry.auto
    ayys: strawberry.auto
    azzs: strawberry.auto
    ayzs: strawberry.auto
    phi: strawberry.auto
    i1: strawberry.auto
    i2: strawberry.auto
    ir1: strawberry.auto
    ir2: strawberry.auto
    # shear_y = fields.DecimalField(max_digits=9, decimal_places=3)
    # shear_z = fields.DecimalField(max_digits=9, decimal_places=3)
    shear_center: tuple[float, float]
    it: strawberry.auto
    awwm: strawberry.auto


@strawberry.experimental.pydantic.type(model=FramePointSchema)
class FramePointType:
    id: strawberry.auto
    y: strawberry.auto
    z: strawberry.auto
    starts_segments: Optional[List["FrameSegmentType"]]
    ends_segments: Optional[List["FrameSegmentType"]]


@strawberry.experimental.pydantic.type(model=FrameSegmentSchema)
class FrameSegmentType:
    id: strawberry.auto
    start_point: 'FramePointType'
    end_point: 'FramePointType'
    thick: strawberry.auto


@strawberry.experimental.pydantic.type(model=FrameSchema)
class FrameType:
    id: strawberry.auto
    frame_pos: strawberry.auto
    cs_values: Optional["FrameCSValuesType"]
    frame_segments: Optional[List["FrameSegmentType"]]
    frame_points: Optional[List["FramePointType"]]


@strawberry.experimental.pydantic.type(model=ShipSchema)
class ShipType:
    id: strawberry.auto
    title: strawberry.auto
    description: strawberry.auto
    author: 'UserType'
    frames: Optional[List["Frame"]]


@strawberry.experimental.pydantic.input(model=ShipSchemaCreate, all_fields=True)
class ShipInput:
    pass


@strawberry.experimental.pydantic.type(model=UserSchema)
class UserType:
    id: strawberry.auto
    username: strawberry.auto
    full_name: strawberry.auto
    notes: Optional[List["NoteType"]]
    ships: Optional[List["ShipType"]]


@strawberry.experimental.pydantic.input(model=UserSchemaCreate, all_fields=True)
class UserInput:
    pass
    # username: strawberry.auto
    # full_name: strawberry.auto
    # password: strawberry.auto
    # created_at: datetime
    # modified_at: datetime
    # is_active: bool
    # is_superuser: bool
    # # notes: fields.ReverseRelation["Note"]
    # ships: Optional[List[ShipType]]


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, id: int) -> UserType:
        user: UserSchema = await UserSchema.from_orm(User.get(id=id))
        return UserType.from_pydantic(user)

    @strawberry.field
    async def get_ship(self, id: int) -> ShipType:
        ship: ShipSchema = await ShipSchema.from_tortoise_orm(Ship.get(id=id))
        return ShipType.from_pydantic(ship)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, user: UserInput) -> UserType:
        hashed_password = get_password_hash(user.password)

        try:
            user_obj = await User.create(
                **{"username": user.username, "full_name": user.full_name, "hashed_password": hashed_password})
        except IntegrityError:
            raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

        return UserType.from_pydantic(user_obj)

    @strawberry.mutation
    async def create_ship(self, ship: ShipInput) -> ShipType:
        obj_in: ShipSchemaCreate = ship.to_pydantic(ShipSchemaCreate)
        return ShipType.from_pydantic(Ship.create(obj_in))


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
