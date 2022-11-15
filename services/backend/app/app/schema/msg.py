import strawberry
from typing import Optional

@strawberry.type
class MsgType:
    msg: str
    id: Optional[int]
    type: Optional[str]
