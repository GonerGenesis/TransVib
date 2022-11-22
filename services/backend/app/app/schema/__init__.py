from fastapi import Request, Depends

import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.http import GraphQLHTTPResponse
from strawberry.types import ExecutionResult
from graphql.error.graphql_error import format_error as format_graphql_error
from tortoise.contrib.pydantic import PydanticModel

from app.core.config import get_settings
from app.db.schemas import *
import app.db.functions as funcs
from app.schema.frame import FrameType, FrameInput
from app.schema.frame_csvalues import FrameCSValuesType, FrameCSValuesInput
from app.schema.frame_segment import FrameSegmentType, FrameSegmentInput
from app.schema.frame_point import FramePointType, FramePointInput
from app.schema.ship import ShipType, ShipInput
from app.schema.user import UserType, UserInput


# @strawberry.experimental.pydantic.type(model=FramePointSchema)


# @strawberry.experimental.pydantic.type(model=FrameSegmentSchema)


@strawberry.type
class Query:
    from .user import get_user
    from .ship import get_ship
    from .frame import get_frame
    from .frame_segment import get_segment
    from .frame_point import get_point
    from .frame_csvalues import get_cs_values


@strawberry.type
class Mutation:
    from .user import create_user, update_user, delete_user
    from .ship import create_ship, update_ship, delete_ship
    from .frame import create_frame, update_frame, delete_frame
    from .frame_segment import create_segment, update_segment, delete_segment
    from .frame_point import create_point, update_point, delete_point
    from .frame_csvalues import create_cs_values


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
