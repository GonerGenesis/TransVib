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


#@strawberry.experimental.pydantic.type(model=UserSchema)
@strawberry.type
class UserType:
    id: int
    username: str
    full_name: Optional[str]
    notes: List[Annotated["NoteType", strawberry.lazy(".note")]]
    ships: List[Annotated["ShipType", strawberry.lazy(".ship")]]


@strawberry.experimental.pydantic.input(model=UserSchemaCreate, all_fields=True)
class UserInput:
    pass
    #username: str
    #full_name: Optional[str] = None
    #password: str


@strawberry.experimental.pydantic.input(model=UserSchemaUpdate, all_fields=True)
#@strawberry.input
class UserUpdate:
    pass
    # username: Optional[str] = None
    # full_name: Optional[str] = None


@strawberry.mutation
async def create_user(self, user: UserInput) -> UserType:
    # print(user)
    # user = UserSchemaCreate(username=user.username, full_name=user.full_name, password=user.password)
    user = user.to_pydantic()
    user_obj = await funcs.user.create(user)
    print(user_obj.dict())
    return user_obj

@strawberry.mutation
async def update_user(self, user_id: int, user: UserUpdate) -> UserType:
    # print(user.__dict__)
    dict_in = user.__dict__
    print("before", dict_in)
    dict_in = {key: val for (key, val) in dict_in.items() if val is not None}
    print("after", dict_in)
    print("other", user.to_pydantic())
    # obj_in = UserSchemaUpdate({key: val for key, val in dict_in if val is not UNSET})
    # obj_in = UserSchemaUpdate(username=user.username, full_name=user.full_name)
    # obj_in = UserSchemaUpdate(**dict_in)
    # obj_in = user.to_pydantic()
    # print(obj_in.dict(exclude_unset=True))
    # await User.filter(id=id).update(**obj_in.dict(exclude_unset=True))
    # return await UserSchema.from_queryset_single(User.get(id=id))
    obj_in: UserSchemaUpdate = user.to_pydantic()
    user: UserSchema = await funcs.user.update(id=user_id, obj_in=obj_in)
    return user


@strawberry.field
async def get_user(self, id: int) -> UserType:
    # user = await User.get(id=id)
    # return await UserSchema.from_tortoise_orm(user)
    return await funcs.user.get(id=id)


@strawberry.mutation
async def delete_user(self, id: int) -> MsgType:
    return await funcs.user.delete(id=id)
