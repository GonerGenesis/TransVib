from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

from ..models import User
from ...core.security import get_password_hash


async def create_user(username: str, password: str, full_name: str = ""):
    # print(user)
    hashed_password = get_password_hash(password)

    try:
        user_obj = await User.create(
            **{"username": username, "full_name": full_name, "hashed_password": hashed_password})
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

    return await user_obj


async def get_user_by_id(id: int):
    return await User.get(id=id)
