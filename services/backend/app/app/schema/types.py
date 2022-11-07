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
import app.db.functions as funcs
from app.db.functions.user import get_user_by_id, create_user


@strawberry.experimental.pydantic.type(model=NoteSchema)
class NoteType:
    id: strawberry.auto
    title: strawberry.auto
    content: strawberry.auto
    created_at: strawberry.auto
    modified_at: strawberry.auto


# @strawberry.experimental.pydantic.type(model=FrameCSValuesSchema)
@strawberry.type
class FrameCSValuesType:
    frame: 'FrameType'
    created_at: datetime
    modified_at: datetime
    # y = fields.DecimalField(max_digits=9, decimal_places=3)
    # z = fields.DecimalField(max_digits=9, decimal_places=3)
    center: tuple[float, float]
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
    shear_center: tuple[float, float]
    it: float
    awwm: float


# @strawberry.experimental.pydantic.type(model=FramePointSchema)
@strawberry.type
class FramePointType:
    id: int
    y: float
    z: float
    starts_segments: Optional[List["FrameSegmentType"]]
    ends_segments: Optional[List["FrameSegmentType"]]


# @strawberry.experimental.pydantic.type(model=FrameSegmentSchema)
@strawberry.type
class FrameSegmentType:
    id: int
    start_point: 'FramePointType'
    end_point: 'FramePointType'
    thick: float


# @strawberry.experimental.pydantic.type(model=FrameSchema)
@strawberry.type
class FrameType:
    id: int
    frame_pos: float
    cs_values: Optional["FrameCSValuesType"]
    frame_segments: Optional[List["FrameSegmentType"]]
    frame_points: Optional[List["FramePointType"]]


# @strawberry.experimental.pydantic.type(model=ShipSchema)
@strawberry.type
class ShipType:
    id: int
    title: str
    description: Optional[str]
    author: 'UserType'
    frames: Optional[List["FrameType"]]


@strawberry.experimental.pydantic.input(model=ShipSchemaCreate, all_fields=True)
class ShipInput:
    pass


# @strawberry.experimental.pydantic.type(model=UserSchema)
@strawberry.type
class UserType:
    id: int
    username: str
    full_name: Optional[str]
    notes: Optional[List["NoteType"]]
    ships: Optional[List["ShipType"]]


# @strawberry.experimental.pydantic.input(model=UserSchemaCreate, all_fields=True)
@strawberry.input
class UserInput:
    username: str
    full_name: Optional[str] = None
    password: str
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
        # user = await User.get(id=id)
        # return await UserSchema.from_tortoise_orm(user)
        return await funcs.user.get_user_by_id(id=id)

    @strawberry.field
    async def get_ship(self, id: int) -> ShipType:
        return await funcs.ship.get(id=id)

    @strawberry.field
    async def get_point(self, id: int) -> ShipType:
        return await funcs.point.get(id=id)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, user: UserInput) -> UserType:
        user_obj = await funcs.user.create_user(user.username, user.password, user.full_name)
        return user_obj

    @strawberry.mutation
    async def create_ship(self, ship: ShipInput) -> ShipType:
        ship_obj = await funcs.ship.create(ship.to_pydantic())
        return ship_obj


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
