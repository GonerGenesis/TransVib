from datetime import datetime
from typing import Optional, List

import strawberry
from strawberry.fastapi import GraphQLRouter

from app.db.functions.ship import get_ship, create_ship
from app.db.functions.user import get_user_by_id, create_user


@strawberry.type
class ShipSchema:
    id: Optional[int]
    title: str
    description: str
    author: 'UserSchema'
    # frames: Optional[List["Frame"]]


@strawberry.type
class UserSchema:
    id: Optional[int]
    username: str
    full_name: Optional[str]
    created_at: datetime
    modified_at: datetime
    is_active: bool
    is_superuser: bool
    # notes: fields.ReverseRelation["Note"]
    ships: Optional[List[ShipSchema]]


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
