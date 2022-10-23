from datetime import datetime
from typing import Optional, List

from pydantic import condecimal
from sqlmodel import SQLModel, Field, Relationship

from models import Ship


class Frame(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    frame_pos: condecimal(max_digits=9, decimal_places=3) = Field(index=True)
    updated: datetime = Field(default=datetime.utcnow())
    ship_id: Optional[int] = Field(default=None, foreign_key="ship_id")
    ship: Ship = Relationship(back_populates="frames")