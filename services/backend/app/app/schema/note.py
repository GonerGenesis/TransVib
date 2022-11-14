import datetime

import strawberry


@strawberry.type
class NoteType:
    id: int
    title: str
    content: str
    created_at: datetime.datetime
    modified_at: datetime.datetime
