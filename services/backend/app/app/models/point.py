from typing import Optional, List
from sqlmodel import (SQLModel, Field, create_engine, Relationship)
from app.core.config import get_settings

class Point(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    frame