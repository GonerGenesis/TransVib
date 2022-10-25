from datetime import datetime
from typing import Optional, List

import strawberry
from . import ShipSchema


@strawberry.type
class UserSchema:
    id: Optional[int]
    username: str
    full_name: Optional[str]
    created_at: datetime
    modified_at: datetime
    is_active: bool
    is_superuser: bool
    # notes: fields.ReverseRelation["Note"]
    ships: Optional[List[ShipSchema]]
