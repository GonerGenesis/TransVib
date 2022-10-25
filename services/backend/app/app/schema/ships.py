from typing import Optional, List

import strawberry


@strawberry.type
class ShipSchema:
    id: Optional[int]
    title: str
    description: str
    author: str
    # frames: List["Frame"]

