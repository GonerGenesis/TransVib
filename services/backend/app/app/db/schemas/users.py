from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import User


class UserSchemaCreate(BaseModel):
    username: str
    full_name: Optional[str]
    password: str


UserSchema = pydantic_model_creator(
    User, name=f"{User.__name__}Schema", exclude=["hashed_password", "created_at", "modified_at"]
)
UserSchemaDatabase = pydantic_model_creator(
    User, name="User", exclude=["created_at", "modified_at"]
)
