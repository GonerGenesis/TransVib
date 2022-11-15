from typing import Optional, List, Annotated, TYPE_CHECKING

import strawberry
from strawberry import UNSET

from .msg import MsgType
from ..db.models import User
from ..db.schemas import UserSchemaCreate, UserSchemaUpdate, UserSchema
from ..db import functions as funcs

if TYPE_CHECKING:
    from .ship import ShipType
    from .note import NoteType


# @strawberry.experimental.pydantic.type(model=UserSchema)
@strawberry.type
class UserType:
    id: int
    username: str
    full_name: str
    notes: List[Annotated["NoteType", strawberry.lazy(".note")]]
    ships: List[Annotated["ShipType", strawberry.lazy(".ship")]]


@strawberry.experimental.pydantic.input(model=UserSchemaCreate)
class UserInput:
    username: str
    full_name: Optional[str] = None
    password: str


#@strawberry.experimental.pydantic.input(model=UserSchemaUpdate)
@strawberry.input
class UserUpdate:
    username: Optional[str] = strawberry.UNSET
    full_name: Optional[str] = strawberry.UNSET


@strawberry.mutation
async def create_user(self, user: UserInput) -> UserType:
    # print(user)
    user = UserSchemaCreate(username=user.username, full_name=user.full_name, password=user.password)
    user_obj: UserSchema = await funcs.user.create(user)
    return user_obj

@strawberry.mutation
async def update_user(self, user_id: int, user: UserUpdate) -> UserType:
    print(user.__dict__)
    dict_in = user.__dict__
    # print(dict_in)
    dict_in = {key: val for (key, val) in dict_in.items() if val is not UNSET}
    # print(dict_in)
    # obj_in = UserSchemaUpdate({key: val for key, val in dict_in if val is not UNSET})
    # obj_in = UserSchemaUpdate(username=user.username, full_name=user.full_name)
    # obj_in = UserSchemaUpdate(**dict_in)
    # obj_in = user.to_pydantic()
    # print(obj_in.dict(exclude_unset=True))
    # await User.filter(id=id).update(**obj_in.dict(exclude_unset=True))
    # return await UserSchema.from_queryset_single(User.get(id=id))
    user: UserSchema = await funcs.user.update(id=user_id, obj_in=UserSchemaUpdate(**dict_in))
    return user


@strawberry.field
async def get_user(self, id: int) -> UserType:
    # user = await User.get(id=id)
    # return await UserSchema.from_tortoise_orm(user)
    return await funcs.user.get(id=id)


@strawberry.mutation
async def delete_user(self, id: int) -> MsgType:
    return await funcs.user.delete(id=id)
