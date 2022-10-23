from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class Ship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]
    frames: List["Frame"] = Relationship(back_populates="point")
