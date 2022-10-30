import logging

import strawberry
from strawberry.fastapi import GraphQLRouter

from ..db.functions.user import create_user, get_user_by_id
from ..db.functions.ship import create_ship, get_ship

from tortoise import Tortoise

log = logging.getLogger("uvicorn")

from .ships import *
from .users import *


# from .frames import *
# from .points import *
# from .segments import *
# from .csvalues import *

@strawberry.type
class Query:
    get_user: UserSchema = strawberry.field(resolver=get_user_by_id)
    get_ship: ShipSchema = strawberry.field(resolver=get_ship)


@strawberry.type
class Mutation:
    create_user: UserSchema = strawberry.field(resolver=create_user)
    create_ship: ShipSchema = strawberry.field(resolver=create_ship)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)
