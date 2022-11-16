from fastapi import HTTPException
from tortoise.exceptions import IntegrityError
from tortoise import connections

from .base import CRUDBase
from ..models import User
from ..schemas import UserSchemaCreate, UserSchema, UserSchemaUpdate
from ...core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserSchema, UserSchemaCreate, UserSchemaUpdate]):
    async def create(self, user: UserSchemaCreate) -> UserSchema:
        hashed_password = get_password_hash(user.password)

        try:
            user_obj = await User.create(
                **{"username": user.username, "full_name": user.full_name, "hashed_password": hashed_password})
        except IntegrityError:
            raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

        return await UserSchema.from_tortoise_orm(user_obj)


user = CRUDUser(User, UserSchema)
# async def get_user_by_id(id: int):
#     return await User.get(id=id)
