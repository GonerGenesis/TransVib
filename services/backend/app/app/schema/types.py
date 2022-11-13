from datetime import datetime
from http.client import NOT_FOUND
from typing import Optional, List
from fastapi import Request

import strawberry
from fastapi import HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.http import GraphQLHTTPResponse
from strawberry.types import ExecutionResult
from graphql.error.graphql_error import format_error as format_graphql_error
from tortoise.contrib.pydantic import PydanticModel
from tortoise.exceptions import IntegrityError

from app.core.security import get_password_hash
from app.db.schemas import *
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
    frame: 'FrameType'
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


# @strawberry.experimental.pydantic.type(model=FramePointSchema)
@strawberry.type
class FramePointType:
    id: int
    y: float
    z: float
    starts_segments: Optional[List["FrameSegmentType"]]
    ends_segments: Optional[List["FrameSegmentType"]]


@strawberry.experimental.pydantic.input(model=FramePointSchemaCreate, all_fields=True)
class FramePointInput:
    pass


# @strawberry.experimental.pydantic.type(model=FrameSegmentSchema)
@strawberry.type
class FrameSegmentType:
    id: int
    start_point: 'FramePointType'
    end_point: 'FramePointType'
    thick: float


@strawberry.experimental.pydantic.input(model=FrameSegmentSchemaCreate, all_fields=True)
class FrameSegmentInput:
    pass


# @strawberry.experimental.pydantic.type(model=FrameSchema)
@strawberry.type
class FrameType:
    id: int
    frame_pos: float
    cs_values: Optional["FrameCSValuesType"]
    frame_segments: Optional[List["FrameSegmentType"]]
    frame_points: Optional[List["FramePointType"]]


@strawberry.experimental.pydantic.input(model=FrameSchemaCreate, all_fields=True)
class FrameInput:
    pass


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
    async def get_frame(self, id: int) -> FrameType:
        return await funcs.point.get(id=id)

    @strawberry.field
    async def get_segment(self, id: int) -> FrameSegmentType:
        return await funcs.segment.get(id=id)

    @strawberry.field
    async def get_point(self, id: int) -> FramePointType:
        return await funcs.point.get(id=id)

    @strawberry.field
    async def get_cs_values(self, id: int) -> FrameCSValuesType:
        from app.db.models import FrameCSValues
        model = await FrameCSValues.filter(frame_id=id).first()

        if not model:
            raise Exception("item not found")

        if issubclass(FrameCSValuesSchema, PydanticModel):
            return await FrameCSValuesSchema.from_tortoise_orm(model)
        return model
        # return await funcs.csvalues.get(frame_id=id)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, user: UserInput) -> UserType:
        # print(user)
        user = UserSchemaCreate(username=user.username, full_name=user.full_name, password=user.password)
        user_obj = await funcs.user.create_user(user)
        return user_obj

    @strawberry.mutation
    async def create_ship(self, ship: ShipInput) -> ShipType:
        ship_obj = await funcs.ship.create(ship.to_pydantic())
        return ship_obj

    @strawberry.mutation
    async def create_frame(self, frame: FrameInput) -> FrameType:
        frame_obj = await funcs.frame.create(frame.to_pydantic())
        return frame_obj

    @strawberry.mutation
    async def create_segment(self, segment: FrameSegmentInput) -> FrameSegmentType:
        segment_obj = await funcs.segment.create(segment.to_pydantic())
        return segment_obj

    @strawberry.mutation
    async def create_point(self, point: FramePointInput) -> FramePointType:
        point_obj = await funcs.point.create(point.to_pydantic())
        return point_obj

    @strawberry.mutation
    async def create_cs_values(self, cs_values: FrameCSValuesInput) -> FrameCSValuesType:
        cs_values_obj = await funcs.csvalues.create(cs_values)
        return cs_values_obj


schema = strawberry.Schema(query=Query, mutation=Mutation)


class MyGraphQLRouter(GraphQLRouter):

    async def process_result(
            self, request: Request, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        data: GraphQLHTTPResponse = {"data": result.data}

        if result.errors:
            data["errors"] = [format_graphql_error(err) for err in result.errors]

        return data


graphql_app = GraphQLRouter(schema)
