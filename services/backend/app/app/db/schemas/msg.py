from typing import Optional

from pydantic import BaseModel


class Msg(BaseModel):
    msg: str
    id: Optional[int]
    type: Optional[str]
