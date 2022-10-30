from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import Ship


class UpdateShip(BaseModel):
    title: Optional[str]
    description: Optional[str]

    # class ShipSchemaCreate(BaseModel):
    #     title: str = None
    #     description: str = None
    #     author_id: int = None


ShipSchemaCreate = pydantic_model_creator(
    Ship, name=f"{Ship.__name__}SchemaCreate", exclude_readonly=True
)

ShipSchema = pydantic_model_creator(
    Ship, name=f"{Ship.__name__}Schema"
)

    # class ShipSchemaCreate(BaseModel):
    #     title: str = None
    #     description: str = None
    #     author_id: int = None
