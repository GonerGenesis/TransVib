import logging

import strawberry
from strawberry.fastapi import GraphQLRouter

from ..db.functions.user import create_user

from tortoise import Tortoise

log = logging.getLogger("uvicorn")

from .ships import *
from .users import *


# from .frames import *
# from .points import *
# from .segments import *
# from .csvalues import *

@strawberry.type
class Mutation:
    create_user: UserSchema = strawberry.field(resolver=create_user)


schema = strawberry.Schema(mutation=Mutation)

graphql_app = GraphQLRouter(schema)
