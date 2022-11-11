from fastapi import HTTPException
from tortoise.exceptions import IntegrityError
from tortoise import connections

from ..models import User
from ..schemas import UserSchemaCreate
from ...core.security import get_password_hash


async def create_user(user: UserSchemaCreate):
    # print(user)
    hashed_password = get_password_hash(user.password)

    try:
        print(connections.)
        user_obj = await User.create(
            **{"username": user.username, "full_name": user.full_name, "hashed_password": hashed_password})
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

    return await user_obj


async def get_user_by_id(id: int):
    return await User.get(id=id)
