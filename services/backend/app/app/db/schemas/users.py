from typing import Optional

from pydantic import BaseModel, validator, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import User


class UserSchemaCreate(BaseModel):
    username: str
    full_name: Optional[str]
    password: str

    @validator('username', 'full_name', 'password')
    def field_not_empty(cls, v):
        # print(v)
        if not (v and v.strip()):
            raise ValueError('field doesn\'t accept empty string')
        return v


class UserSchemaUpdate(BaseModel):
    username: Optional[str]
    full_name: Optional[str]

    @validator('username', 'full_name')
    def field_not_empty(cls, v):
        # print(v)
        if v == '':
            raise ValueError('field doesn\'t accept empty string')
        return v


UserSchema = pydantic_model_creator(
    User, name=f"{User.__name__}Schema", exclude=["hashed_password", "created_at", "modified_at"]
)
UserSchemaDatabase = pydantic_model_creator(
    User, name="User", exclude=["created_at", "modified_at"]
)
